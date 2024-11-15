# Checkpoint

## Change 1:

We decided to decouple the points system service from the users service, in order to to mitigate race conditions for reading and writing to the database.

## Change 2:

for reports:
Location
datetime
change UEN to author
