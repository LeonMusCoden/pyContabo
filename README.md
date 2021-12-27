# pyContabo
basic python wrapper for the [Contabo API](https://api.contabo.com/#section/Introduction).

This wrapper is incomplete. 
The following api funtions have been implemented:
- List instances
- Get specific instance by id
- Instance Actions
- List snapshots
- Create a new instance snapshot
- Retrieve a specific snapshot by id
- Delete existing snapshot by id
- Rollback the instance to a specific snapshot by id

The API for snapshots is currently broken. All of the snapshot function are therefore untested.
All the naming is similar to the documentation provided by Contabo. 
