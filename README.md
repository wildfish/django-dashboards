# Datorum

Initial work on the Datorum idea of building a toolkit/possible open source project to support Django dash like dashboards. 

## Plan

### Richard's initial use cases 

- Auto-generate a useful grid-based layout based on a default template and stylesheet with simple customisations
- Manually write a template and include specific components in specific places
- Send a list of components to an SPA frontend where the React will do both of the above

### Designs 

https://drive.google.com/drive/u/0/folders/0AFOShL-qRZlcUk9PVA

## High level overview

- `/django-datorum/datorum` is the library, which will eventually become this os project, the tool we install in clients projects.
  - Only holds a couple of basic components atm.
    - Handles grid, div and custom layouts
    - Layout class can be used to make the same dashboard display differently
      - Allows for simple grouped components
  - Uses HTMX, very basic atm but the idea being we take it further as the use cases expand.
  - More specific notes/todos in `/django-datorum/README.md`
- `/demo`is a Django MPA using `datorum` to mock up how we'd use the lib 
  - Note that for ease the graphql endpoint for the SPA is also part of this Django project.
- `/demo-spa` is a Next.js version of demo, using `datorum` and graphql to fetch the structure. 
- Will eventually be split 2 3 repos, all in one for ease atm.

## Current progress & todo 

### General (and MPA)

* Documentation 
* Registry 
  * Done but no auto view approach atm. 
* Websockets
  * Experimented with but we need a real world, ideally it would work for any component as an alternative to defer/value potentially. 
* Permissions 
  * Dashboard level classes added, needs adding to demo.
* Performance
* Dashboard/top level filtering.   
* Test coverage - needs a lot more
  * CI
  * Tests for the 2 demos 
* Transformers/data?
  * How can we map data into components, helper functions or something more complex at a component level? 
  * Maybe we sit all this sep as the proprietary side? 


  
### Components

* Text, HTML & Stat - Done. 
* Chart
  * Plotly only atm
  * Handles gauges also.
  * Rename to Chart   
  * Need to decided on where option/layout control is defined, leaning towards parameterising what we want in the component.
    * labels etc 
    * custom tooltips
* Table
  * Added via tabulator. 
  * Ajax data added, pagination and sorting added. 
  * Filtering to do.
  * Same as charts where does option control live, parameterising is the way I've started to go.
    * Column headers etc 
    * Sortable fields. 
  * Adding helpers to map data to expected? This is a general question 
  * Clickable columns/links or at least safe HTML data displaying. 
* Map 
  * Mapbox via plotly? 
* Component grouping - done. 
* Component filtering - done. 
* Dependent components - done.
* CTA components
* Icons on components

### Demo & SPA

* Demo 
  * Menu 
  * Permissions 
* SPA 
  * Bring to same point as MPA 
    * Table example 
    * Grouped

## Development  

### Demo 

```
cd demo
pyenv virtualenv 3.9.9 django-datorum-demo
pyenv activate django-datorum-demo
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata flat_text.json
python manage.py runserver
```

### Demo  SPA

Running backend as above

```
cd demo_spa
yarn install
yarn dev
```

Docker is in the repo as per our template, but I've not been using it so far so likely needs some work. It also would need the spa adding. 

### SSE / Websockets 

See datorum/README.md