import React, {useContext, useMemo} from "react";
import {useTable, useSortBy, usePagination} from 'react-table'
import * as styles from "@/components/component/table/index.module.scss";
import {FilterContext} from "../../../appContext";

export const ReactTable = ({component, value}: { component: any, value: any }) => {
    const componentKey = component.key;
    let valueJson = JSON.parse(JSON.stringify(value));
    let data = valueJson.data;
    let paging = valueJson.paging;
    let columns = [];
    if (data.length > 0) {
        columns = useMemo(
            () => Object.keys(data[0]).map(k => {
                return {Header: k, accessor: k}
            }),
            [data]
        )
    }

    return <Table componentKey={componentKey} columns={columns} data={data} paging={paging}/>
}

const PaginationButtons = ({
                               gotoPage,
                               canPreviousPage,
                               previousPage,
                               nextPage,
                               canNextPage,
                               pageCount,
                               pageIndex,
                               pageOptions
                           }: { gotoPage: any, canPreviousPage: boolean, previousPage: any, nextPage: any, canNextPage: boolean, pageCount: number, pageIndex: number, pageOptions: any }) => {
    return (
        <div className={styles.pagination}>
            <button onClick={() => previousPage()} disabled={!canPreviousPage}>
                Previous
            </button>
            {" "}
            <button onClick={() => nextPage()} disabled={!canNextPage}>
                Next
            </button>
            {" "}
            <span>
            Page{" "}
                <strong>
        {pageIndex + 1} of {pageCount}
            </strong>{" "}
            </span>
        </div>

    )
}

const Table = ({componentKey, columns, data, paging}: { componentKey: string, columns: [], data: [], paging: any }) => {
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
                pageSize: paging?.page_size ?? 10,
            },
            manualPagination: paging?.ssr ?? false,
            manualSortBy: paging?.ssr ?? false,
            autoResetPage: false,
            pageCount: paging?.page_count ?? 1,
        },
        useSortBy,
        usePagination
    )

    const {pageIndex, pageSize, sortBy} = state;
    const [filters, setFilter] = useContext(FilterContext)

    React.useEffect(() => {
        const newFilters = [componentKey].reduce((a, b) => {
            a[b] = {...a[b], length: pageSize, start: pageIndex * pageSize}
            return a
        }, {...filters})
        // update the filters for the table
        setFilter(newFilters)
    }, [componentKey, pageIndex, pageSize]);

    React.useEffect(() => {
        if (sortBy.length > 0) {
            const sortParams = sortBy[0];
            let sortById = sortParams.id
            const sortyByDir = sortParams.desc ? 'desc' : 'asc'
            const newFilters = {[componentKey]: {...filters[componentKey], sortby: sortById, direction: sortyByDir}}
            // update the filters for the table
            setFilter(newFilters)
        }
    }, [componentKey, sortBy]);

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