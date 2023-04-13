import polars as pl
import networkx as nx
import leidenalg
import igraph as ig


def get_community(transfer_df, year, end_year=None):
    """
    Using RBConfigurationVertexPartition of leidenalg
    to get the community partition of each countries

    Parameters:
    -----------
    transfer_df : polars dataframe
        A polars dataframe that holds all the arms transfer data.
        Should be the data from the file joined_data.csv

    year : int
        The target year of data where the community detection would run on.
        If `end_year` is not specified, only the data for this year is considered.

    end_year : int, optional
        The end year of the range of years when the community detection would run on.
        If specified, the function will consider a range of years from `year` to `end_year`.

    Returns:
    --------
    partition : Dict

        the partition of the countries

        key : int
            the index of community

        value : List of strings
            the list of countries that belong to community in the index
            note that may contain names of several non gov organizations such as rebel groups

    name_index : Dict

        the index of each country name

        key : string
            the name of countries

        value : int
            the index of node
    """

    # If `end_year` is not specified, set it to be the same as `year`
    if end_year is None:
        end_year = year
    elif end_year < year:
        raise ValueError(f"End year: {end_year} cannot be earlier than start year: {year}.")

    # filter the data that in the specific year range
    year_df = transfer_df.filter((pl.col("Order date") >= year) &
                                 (pl.col("Order date") <= end_year))

    # add transfers to a DiGraph
    # not the weight of each transfer use the TIV delivery values from the dataset
    # direction is set as Buyer -> Seller
    G = nx.DiGraph()

    for row in year_df.rows(named=True):
        G.add_edge(row['Buyer'], row['Seller'], weight=row['TIV delivery values'])

    # convert DiGraph to iGraph which is suitable for leidenalg
    # keep the direction of the graph
    ig_graph = ig.Graph.TupleList(G.edges(), directed=True)

    # get the partition with the leidenalg
    partition = leidenalg.find_partition(ig_graph,
                                         leidenalg.VertexPartition.RBConfigurationVertexPartition)

    # Create a dictionary to map node names to node indices
    name_index = {name: index for index, name in enumerate(ig_graph.vs['name'])}

    return partition, name_index


if __name__ == '__main__':
    df = pl.read_csv("../rtf/joined_data.csv")
    example_parti, name_to_index = get_community(df, 1992, end_year=2020)
    print(example_parti)

    example_node = "United States"

    # example on get the community of a sample node
    # get the index of node from the name_index first
    # then get the community index from the membership of the partition
    print(f"Node {example_node} belongs to community {example_parti.membership[name_to_index[example_node]]}")
