import React, { useState } from 'react';

const FilterContext = React.createContext([{}, () => {}]);

const FilterProvider = (props) => {
  const [filters, setFilter] = useState({});
  return (
    <FilterContext.Provider value={[filters, setFilter]}>
      {props.children}
    </FilterContext.Provider>
  );
}

export { FilterContext, FilterProvider };