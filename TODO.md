This script is only good for initial setup.
Problems:
- Not sure if we're actually getting all cases
- Not sure if we're getting all case details, unable to parse some cases
- Slow

Create database to house case details + attachments
Web crawler for attachments
Daily update script
- Check for new cases (7 day lookback. Selenium or page search requests > depends on if we want case details)
- Check for updates for open cases. 
- Check for updates for closed cases less frequently.

Would it make sense to build on top of github.com/labordata/nlrb-data database?
- They have more info than just details
- they have a daily update
- they don't have cases prior to 2010
- I don't know anything about  nlrb data