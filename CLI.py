import click
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="source_open",
    auth_plugin="mysql_native_password",
)

params = {
    "headline": "",
    "authorName": "",
    "url": "",
    "claimType": "",
    "numCitations": "",
    "publisherName": "",
    "publicationDate": "",
    "startDate": "",
    "endDate": "",
    "authorID": "",
    "articleID": "",
}

cursor = db.cursor(buffered=True)


def send_query(query):
    cursor.execute(query)
    return cursor.fetchall()


def display_article_specs():
    click.echo("\n--- Article Specs ---")

    # search options
    searchParams = False
    while not searchParams:
        search_headline = click.confirm("Search by words in Headline?")
        if search_headline:
            headline = click.prompt("Enter the words to search")
        search_author_name = click.confirm("Search by Author Name?")
        if search_author_name:
            author_name = click.prompt("Enter the Author's Name")

        if any([search_headline, search_author_name]):
            searchParams = True

        if not any([search_headline, search_author_name]):
            click.echo("Please select at least one option.")

    # display options
    displayDeets = False
    while not displayDeets:
        display_headline = click.confirm("Display Headline?")
        display_url = click.confirm("Display URL?")
        display_author_name = click.confirm("Display Author Name?")
        if any([display_headline, display_url, display_author_name]):
            displayDeets = True
        if not any([display_headline, display_url, display_author_name]):
            click.echo("Please select at least one option.")

    # building the query
    """select_clause = ""
    if display_headline:
        select_clause += ", headline"
    if display_url:
        select_clause += ", AD.url"
    if display_author_name:
        select_clause += ", authorName"
    if select_clause.startswith(","):
        select_clause = select_clause[2:]
        
    from_clause = "article AS A, articleDetails AS AD, Author AS Au, WrittenBy AS W"
    
    where_clause = "A.url = AD.url AND A.articleID = W.articleID AND W.authorID = Au.authorID"
    if search_headline:
        where_clause += " AND headline LIKE '%" + headline + "%'"
    if search_author_name:
        where_clause += " AND authorName LIKE '%" + author_name + "%'"
    
    query = "SELECT " + select_clause + " FROM " + from_clause + " WHERE " + where_clause + ";"
    for row in send_query(query):
        string = ""
        for i in range(len(row)):
            string += str(row[i]) + " | "
        click.echo(string)    """


def display_claims():
    click.echo("\n--- Claims ---")
    display_text = click.confirm("Display Text?")
    display_claim_type = click.confirm("Display Type of Claim?")
    display_num_citations = click.confirm("Display #Citations?")
    filter_by_citations = click.confirm("Filter by >= No. of Citations?")

    if not any(
        [display_text, display_claim_type, display_num_citations, filter_by_citations]
    ):
        click.echo("Please select at least one option.")
    else:
        if display_claim_type:
            filter_claim_type = click.confirm("Filter by a particular type of claim?")
            if filter_claim_type:
                claim_type_options = ["Primary", "Secondary", "Tertiary"]
                claim_type = click.prompt(
                    "Select a claim type", type=click.Choice(claim_type_options)
                )
                # Add code to handle filtering by claim type here

        if filter_by_citations:
            min_citations = click.prompt(
                "Enter the minimum number of citations", type=int
            )
            # Add code to handle filtering by citations here

        # Add code to handle the other selected options for Claims here


def display_publisher_details():
    click.echo("\n--- Publisher Details ---")
    display_publisher_name = click.confirm("Display Publisher Name?")
    display_publication_date = click.confirm("Display Publication Date?")

    if not any([display_publisher_name, display_publication_date]):
        click.echo("Please select at least one option.")
    else:
        if display_publisher_name:
            search_publisher_name = click.confirm("Search by Publisher Name?")
            if search_publisher_name:
                publisher_name = click.prompt("Enter the Publisher's Name")
                # Add code to handle searching by publisher name here

        if display_publication_date:
            filter_by_date_range = click.confirm("Filter by Publication Date range?")
            if filter_by_date_range:
                start_date = click.prompt("Enter the start date (YYYY-MM-DD)")
                end_date = click.prompt("Enter the end date (YYYY-MM-DD)")
                # Add code to handle filtering by publication date range here

        # Add code to handle the other selected options for Publisher Details here


def main():
    click.echo("Welcome to SOURCE-OPEN!\n")

    while True:
        click.echo("Select an option:")
        click.echo("1. Article Specs")
        click.echo("2. Claims")
        click.echo("3. Publication Details")
        click.echo("4. Quit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            display_article_specs()
        elif choice == 2:
            display_claims()
        elif choice == 3:
            display_publisher_details()
        elif choice == 4:
            click.echo("Exiting Source-Open. Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please select a valid option.\n")


if __name__ == "__main__":
    main()
