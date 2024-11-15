import ollama
import aiofiles
import asyncio
import numpy as np
import pandas as pd


class OllamaChat:
    def __init__(self, model_name: str):
        # Initialize with a model name for text or image analysis
        self.model_name = model_name
        self.auth_df = pd.read_csv("database/authorities.csv")
        self.authorities_list = [
            "Police Station",
            "Fire Station",
            "Community Center",
            "Hospital",
            # "Emergency Services",
        ]

    async def ask(self, prompt: str) -> str:
        # Generate a text response using ollama asynchronously
        response = await asyncio.to_thread(
            ollama.generate, model=self.model_name, prompt=prompt
        )
        return response["response"]  # Return only the 'response' part

    async def analyze_image(self, image_path: str, prompt: str) -> str:
        # Open the image in binary mode asynchronously
        async with aiofiles.open(image_path, "rb") as image_file:
            image_data = await image_file.read()

        # Generate response based on the image and prompt using the 'llava' model asynchronously
        response = await asyncio.to_thread(
            ollama.generate,
            model="llava",  # Use 'llava' for image-based prompts
            prompt=prompt,
            images=[image_data],  # Pass image as bytes
        )
        return response["response"]  # Return only the 'response' part

    async def compare_analysis_and_description(
        self, image_analysis: str, text_description: str
    ) -> str:
        # Generate a prompt for comparison to get numeric ratings for relevance, severity, and urgency
        prompt = (
            f"Based on the details below, please rate each aspect for a fault report:\n\n"
            f"Image Analysis: {image_analysis}\n\n"
            f"Text Description: {text_description}\n\n"
            f"1. **Relevance**: Rate how closely the text description matches the content of the image (1-10).\n"
            f"   - 1: Completely unrelated\n"
            f"   - 5: Partially relevant\n"
            f"   - 10: Highly relevant\n\n"
            f"2. **Severity**: Rate the level of seriousness or potential harm depicted in the image (1-10).\n"
            f"   - 1: Minor issue with little impact\n"
            f"   - 5: Moderate issue that could cause inconvenience\n"
            f"   - 10: Critical issue with high risk or damage\n\n"
            f"3. **Urgency**: Rate the need for immediate action based on the situation (1-10).\n"
            f"   - 1: No action needed\n"
            f"   - 5: Action needed soon\n"
            f"   - 10: Immediate action required, prioritizing issues where delays could cause irreversible effects, "
            f"       permanent injury, or fatal damage to property\n\n"
            f"Respond only with the numbers in this format: 'X,Y,Z', where:\n"
            f"   - X = Relevance\n"
            f"   - Y = Severity\n"
            f"   - Z = Urgency\n"
        )

        # Get the comparison response asynchronously
        response = await asyncio.to_thread(
            ollama.generate, model=self.model_name, prompt=prompt
        )

        # Return the response as a structured string
        return response["response"].strip()

    async def analyse_image_and_text(
        self, image_path: str, image_prompt: str, text_description: str
    ) -> dict:
        # Analyze an image with a prompt using the 'llava' model asynchronously

        image_prompt = (
            "Provide a brief, factual description of the main action or event occurring in this image. "
            "Only respond with the description. Focus on what is happening, not just what is present, and do not hallucinate or provide factually incorrect information."
        )

        # Await the asynchronous image analysis
        image_analysis = await self.analyze_image(image_path, image_prompt)
        print("Image Analysis Response:", image_analysis)

        # Await the asynchronous comparison for ratings
        ratings = await self.compare_analysis_and_description(
            image_analysis, text_description
        )
        ratings_int = [int(x) for x in ratings.split(",")]

        # Await the asynchronous ask for title generation
        title = await self.ask(
            f"Generate a concise, factual title (under 10 words) for this fault report:\n"
            f"Description: {text_description}\n"
            f"Image analysis: {image_analysis}\n"
            f"Respond with a straightforward and specific title only, like 'Man dies on street' or 'Cat stuck on tree.' Avoid figurative language, assumptions, or additional details."
        )

        return {"ratings": ratings_int, "title": title, "analysis": image_analysis}

    async def find_nearest_authority(
        self, input_lat: float, input_lon: float, authority_type: str
    ) -> dict:
        # Filter the DataFrame by authority type
        filtered_df = self.auth_df[self.auth_df["Type"] == authority_type]
        # Calculate distances using the Haversine formula
        distances: pd.DataFrame = filtered_df.apply(
            lambda row: self.haversine(
                input_lat, input_lon, row["Latitude"], row["Longitude"]
            ),
            axis=1,
        )
        # Get the index of the nearest authority
        nearest_index = distances.idxmin()
        nearest_authority = filtered_df.loc[nearest_index]
        # Return the nearest authority's details
        return {
            "Authority Name": nearest_authority["Authority Name"],
            "Latitude": nearest_authority["Latitude"],
            "Longitude": nearest_authority["Longitude"],
            "Distance (km)": distances[nearest_index],
        }

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371.0  # Earth radius in kilometers
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        delta_phi, delta_lambda = np.radians(lat2 - lat1), np.radians(lon2 - lon1)
        a = (
            np.sin(delta_phi / 2) ** 2
            + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
        )
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        return R * c

    async def get_relevant_authority_ollama(self, description: str, analysis: str) -> str:
        # Create a prompt for Ollama to identify the relevant authority type
        prompt = (
            f"Based on the description below, identify the most relevant authority type from the list. "
            f"Respond only with the exact authority type as written in the list:\n\n"
            f"Description: {description}\n\n"
            f"Analysis: {analysis}\n\n"
            f"Available authority types: {', '.join(self.authorities_list)}\n\n"
            f"Please respond with the most relevant authority type as written."
        )

        # Use the ask method to get the response from Ollama
        response = await self.ask(prompt)

        # Strip any extra whitespace and check if response matches a valid entry in authorities_list
        relevant_authority = response.strip()

        if relevant_authority in self.authorities_list:
            return relevant_authority
        else:
            return "Unknown"
