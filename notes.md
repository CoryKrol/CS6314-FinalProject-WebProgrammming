## User tries to buy stock

a) the stock is in our database
b) the stock is not in our database flag it and let user know an admin must review before approving the sale
    - send administrator email notification when it happens
        - with yes/no buttons to approve/not approve
            -if yes then entered into database with default info the app can get from yahoo finance
                -admin can add product pictures later

## Models
### Stock
#### Fields
- Ticker
- Name of company
- Description
- Industry  
- Last trade price
- 52-week high / 52-week low
- what users have traded it and what market share of it do they have
- stretch goals: stock price graph, stock news

### User
#### New fields/features
- Track total p/l for each stock for each user
- Track total YTD P/L
- Total estimated capitals gains tax
    - Need to distinguish between taxable and tax-deferred accounts

### Templates
#### Display stocks
##### Stock information
- Ticker
- Name of company
- Description
- Industry  
- Last trade price
- 52-week high / 52-week low
- what users have traded it and what market share of it do they have
- stretch goals: stock price graph, stock news
##### Pages that display lists of stocks
######
