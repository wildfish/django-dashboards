import React, {useContext, useMemo} from "react";
import {useTable, useSortBy, usePagination} from 'react-table'
import * as styles from "@/components/component/table/index.module.scss";
import {FilterContext} from "../../../appContext";

export const ReactTable = ({value}: { value: any }) => {
    let valueJson = JSON.parse(JSON.stringify(value));
    let data = valueJson.rows;
    let paging = valueJson.paging;
    const columns = useMemo(
     () => Object.keys(data[0]).map(k => {return {Header: k, accessor: k}}),
     []
    )

    return <Table columns={columns} data={data} paging={paging} />
}

const PaginationButtons = ({gotoPage, canPreviousPage, previousPage, nextPage, canNextPage, pageCount, pageIndex, pageOptions}) => {
    return (
        <div className={styles.pagination}>
            <button onClick={() => previousPage()} disabled={!canPreviousPage}>
                Previous
            </button>{" "}
            <button onClick={() => nextPage()} disabled={!canNextPage}>
            Next
            </button>{" "}
            <span>
            Page{" "}
            <strong>
        {pageIndex + 1} of {pageCount}
            </strong>{" "}
            </span>
      </div>

    )
}

const Table = ({columns, data, paging}) => {
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        page,
        nextPage,
        previousPage,
        canPreviousPage,
        canNextPage,
        pageOptions,
        gotoPage,
        pageCount,
        setPageSize,
        state,
    } = useTable(
        {
            columns,
            data,
            initialState: {
                pageIndex: paging?.page ?? 0,
                pageSize: paging?.limit ?? 10,
                sortBy: paging?.sortby ?? [],
            },
            manualPagination: paging?.ssr ?? false,
            manualSortBy: paging?.ssr ?? false,
            autoResetPage: false,
            pageCount: paging?.page_count ?? 1,
        },
        useSortBy,
        usePagination
    )

    const { pageIndex, pageSize, sortBy } = state;
    const [filters, setFilter] = useContext(FilterContext)

    // only save filters if we are using ssr
    if (paging?.ssr) {
        React.useEffect(() => {
            setFilter(filters => ({...filters, size: pageSize, page: pageIndex}))
        }, [pageIndex, pageSize]);

        React.useEffect(() => {
            if (sortBy.length > 0) {
                const sortParams = sortBy[0];
                let sortById = sortParams.id
                const sortyByDir = sortParams.desc ? 'desc' : 'asc'
                setFilter(filters => ({...filters, sortby: sortById, direction: sortyByDir}))
            }
        }, [sortBy]);
    }

    return (
        <>
            <table {...getTableProps()} className={styles.table}>
                <thead>
                {headerGroups.map(headerGroup => (
                    <tr {...headerGroup.getHeaderGroupProps()}>
                        {headerGroup.headers.map(column => (
                            <th {...column.getHeaderProps(column.getSortByToggleProps())}>
                                {column.render('Header')}
                                <span>
                    {column.isSorted
                        ? column.isSortedDesc
                            ? ' 🔽'
                            : ' 🔼'
                        : ''}
                  </span>
                            </th>
                        ))}
                    </tr>
                ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                {page.map(row => {
                        prepareRow(row);
                        return (
                            <tr {...row.getRowProps()}>
                                {row.cells.map(cell => {
                                    return (
                                        <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                                    )
                                })}
                            </tr>
                        )
                    }
                )}
                </tbody>
            </table>
            {pageCount > 1 &&
                <PaginationButtons
                    gotoPage={gotoPage}
                    canPreviousPage={canPreviousPage}
                    previousPage={previousPage}
                    nextPage={nextPage}
                    canNextPage={canNextPage}
                    pageCount={pageCount}
                    pageIndex={pageIndex}
                    pageOptions={pageOptions}
                />
            }
        </>
    )
}