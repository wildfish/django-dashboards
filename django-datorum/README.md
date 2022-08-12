This would be the datorum lib/open source project we use for all clients.

### What (at least) is needed to make this MVP ready?

- Permissions/auth at Dashboard class level? We could also let people do this at view level. 
- Docs, lots of docs. 
- Better examples
- Components
    - Initial/basic examples added:
      - HTML/Text components 
      - Stats 
      - Charts
          - Handles gauges and any chart type in Plotly atm, all is passed as data which makes it configurable but at the trade off of needing to know plotly, maybe that's not a big deal. 
      - Table
        - Done but needs work around filtering, ordering etc ajax side
      - Grouped components 
    - Todo     
      - Related/dependent components
      - Icons on components  
      - CTA on components  
      - Light CMS/flatpage driven sections? Although this could be part of client code as per demo. 
- Registry driven auto views similar to admin? 
- Dynamic menu? 
- Celery/pipeline example
- SPA example
- Websockets example
- Tests 
- Caching/performance
- Settings
- Decide on graphene vs straberry, main reason for strawberry is grahene is broken for 4 
  atm & is looking a little dead, last release was Dec 2020 


