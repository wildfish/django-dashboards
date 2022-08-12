# Datorum

Initial work on the Datorum idea of building a toolkit/possible open source project to support Django dash like dashboards. 

## Plan

### Richard's initial use cases 

- Auto-generate a useful grid-based layout based on a default template and stylesheet with simple customisations
- Manually write a template and include specific components in specific places
- Send a list of components to an SPA frontend where the React will do both of the above

### Designs 

https://drive.google.com/drive/u/0/folders/0AFOShL-qRZlcUk9PVA

## So far

- `/django-datorum/datorum` is the library, which will eventually become this os project, the tool we install in clients projects.
  - Only holds a couple of basic components atm.
    - Handles grid, div and custom layouts
    - Layout class can be used to make the same dashboard display differently
      - Allows for simple grouped components
  - Uses HTMX, very basic atm but the idea being we take it further as the use cases expand.
  - More specific notes/todos in `/django-datorum/README.md`
- `/demo`is a Django MPA using `datorum` to mock up how we'd use the lib in a Sandvik like way.
  - Note that for ease the graphql endpoint for the SPA is also part of this Django project.
- `/demo-spa` is a Next.js version of demo, using `datorum` and graphql to fetch the structure. 
- Will eventually be split 2 3 repos, all in one for ease atm. 

## Development

### Demo 

```
cd demo
pyenv virtualenv 3.9.9 django-datorum-demo
pyenv activate django-datorum-demo
python manage.py migrate
python manage.py runserver
```

### Demo  SPA

Running backend as above

```
cd demo-spa
yarn install
yarn dev
```

Docker is in the repo as per our template, but I've not been using it so far so likely needs some work. It also would need the spa adding. 
