import React, { useState } from 'react';

const FilterContext = React.createContext([{}, () => {}]);

const FilterProvider = (props) => {
  const [filter, setFilter] = useState({});
  return (
    <FilterContext.Provider value={[filter, setFilter]}>
      {props.children}
    </FilterContext.Provider>
  );
}

export { FilterContext, FilterProvider };