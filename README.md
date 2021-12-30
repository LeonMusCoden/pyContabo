# pyContabo
basic python wrapper for the [Contabo API](https://api.contabo.com/#section/Introduction).

This wrapper is incomplete. 
The following api funtions have been implemented:
- List instances
- Get specific instance by id
- Create instance
- Instance Actions
- List snapshots (The Server-side is currently broken)
- Create a new instance snapshot
- Retrieve a specific snapshot by id* (can't test because snapshot list isn't working)
- update existing snapshot*
- Delete existing snapshot*
- Rollback the instance to a specific snapshot* 

*(can't test because snapshot list isn't working).

Currently, I'm working on Instance and Snapshot Audits to complete the Compute Instances part of the wrapper. 
