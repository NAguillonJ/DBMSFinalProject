import click
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="source_open",
    auth_plugin="mysql_native_password",
)

cursor = db.cursor()

# create a function to send any query to the database
def sendQuery(query):
    cursor.execute(query)
    for row in cursor.fetchall():
        click.echo(row)
    click.echo("\n")


def option1():
    type = click.prompt("Enter the type of claim", type=str)
    # create query based on stored procdure findClaimsByType
    cursor.callproc("FindClaimsByType", [type])
    for result in cursor.stored_results():
        for row in result.fetchall():
            click.echo(row[3])
    click.echo("\n")


def option2():
    type = click.prompt("Enter the type of claim", type=str)
    count = click.prompt("Enter the lower bound", type=int)
    # create query based on stored procdure findClaimsByTypeCitedMoreThan
    cursor.callproc("FindClaimsByTypeAndCitations", [type, count])
    for result in cursor.stored_results():
        for row in result.fetchall():
            click.echo(row[3])
    click.echo("\n")


def option3():
    keyword = click.prompt("Enter the keyword", type=str)
    # create query based on stored procdure findArticlesWithKeywordInHeadline
    cursor.callproc("FindArticlesByKeyword", [keyword])
    for result in cursor.stored_results():
        for row in result.fetchall():
            click.echo(row[0])
    click.echo("\n")


def option4():
    author = click.prompt("Enter the author", type=str)
    # create regular query
    cursor.execute(
        """SELECT AD.Headline, A.URL 
        FROM Article AS A, ArticleDetails AS AD, WrittenBy AS WB, Author AS AT 
        WHERE AD.URL = A.URL 
            AND A.ArticleID = WB.ArticleID 
            AND WB.AuthorID = AT.AuthorID 
            AND AT.AuthorName  = %s;""",
            (author,))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")

def option5():
    publisher = click.prompt("Enter the publisher", type=str)
    start = click.prompt("Enter the start date (YYYY - M - D)", type=str)
    end = click.prompt("Enter the end date", type=str)
    # create query
    cursor.execute("""
                   SELECT AD.Headline, A.URL 
                   FROM Article AS A, ArticleDetails AS AD, Publisher AS P, WrittenBy AS WB 
                   WHERE AD.URL = A.URL
                        AND A.ArticleID = WB.ArticleID 
                        AND AD.PubName = P.PubName 
                        AND AD.PubName = %s
                        AND WB.Date BETWEEN %s 
                        AND %s 
                        ORDER BY WB.Date;""", (publisher, start, end))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")


def option6():
    count = click.prompt("Enter the lower bound", type=int)
    # create query
    cursor.execute("""
                   SELECT AT.AuthorName 
                   FROM Author AS AT, WrittenBy AS WB, Claim AS C, CollectionOf AS CO 
                   WHERE AT.AuthorID = WB.AuthorID 
                        AND WB.ArticleID = CO.ArticleID 
                        AND CO.ClaimID = C.ClaimID 
                        GROUP BY AT.AuthorName 
                        HAVING COUNT(C.numCitations) > %s;""", (count,))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")

def option7():
    type = click.prompt("Enter the type of claim", type=str)
    # create query
    cursor.execute("""
                   SELECT DISTINCT AD.Headline, A.URL 
                   FROM Article AS A, ArticleDetails AS AD, CollectionOf AS CO, Claim AS C 
                   WHERE AD.URL = A.URL 
                        AND A.ArticleID = CO.ArticleID 
                        AND CO.ClaimID = C.ClaimID 
                        AND C.type = %s;""", (type,))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")

def option8():
    author = click.prompt("Enter the author", type=str)
    # create query
    cursor.execute("""
                   SELECT C.type, AD.Headline FROM Article AS A, ArticleDetails AS AD, CollectionOf AS CO, Claim AS C, WrittenBy AS WB, Author AS AT 
                   WHERE AD.URL = A.URL 
                        AND A.ArticleID = CO.ArticleID 
                        AND CO.ClaimID = C.ClaimID 
                        AND A.ArticleID = WB.ArticleID 
                        AND WB.AuthorID = AT.AuthorID 
                        AND AT.AuthorName = %s;""", (author,))
    for row in cursor.fetchall():
        click.echo(row)
    click.echo("\n")


def option9():
    count = click.prompt("Enter the lower bound", type=int)
    start = click.prompt("Enter the start date", type=str)
    end = click.prompt("Enter the end date", type=str)
    author = click.prompt("Enter the author", type=str)
    # create query
    cursor.execute("""
                   SELECT DISTINCT AD.Headline 
                   FROM Article AS A, ArticleDetails AS AD, CollectionOf AS CO, Claim AS C, WrittenBy AS WB, Author AS AT 
                   WHERE AD.URL = A.URL 
                        AND A.ArticleID = CO.ArticleID 
                        AND CO.ClaimID = C.ClaimID 
                        AND A.ArticleID = WB.ArticleID 
                        AND WB.AuthorID = AT.AuthorID 
                        AND AT.AuthorName = %s 
                        AND C.Type = 'Tertiary' 
                        AND C.numCitations > %s 
                        AND WB.Date BETWEEN %s AND %s;""", 
                        (author, count, start, end))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")

def printResults():
    for result in cursor.stored_results():
        for row in result.fetchall():
            click.echo(row[0])
    click.echo("\n")


def main():
    click.echo("Welcome to SOURCE-OPEN!\n")

    while True:
        click.echo("Select an option:")
        click.echo("1. Find all the claims of type _________.")
        click.echo(
            "2. Find all the claims of type _________ cited more than ______ times."
        )
        click.echo("3. Find all the articles which have _________ in Headline.")
        click.echo("4. Find all the articles written by __________ author.")
        click.echo(
            "5. Find all the articles published by __________ publisher between dates _______ and _________ in chronological order."
        )
        click.echo(
            "6. Find the authors whose claims have been cited more than ______ times."
        )
        click.echo(
            "7. Find article headlines and URLs of the articles that have claims of type _____________. "
        )
        click.echo(
            "8. Find all the claims made by _______ author, group them by type, and display the headline of the article in which the claim was made."
        )
        click.echo(
            "9. Find all the article headlines with more than _______ tertiary claims published between ______ and ______ date range, written by ________ author."
        )
        click.echo("10. Quit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            option1()
        elif choice == 2:
            option2()
        elif choice == 3:
            option3()
        elif choice == 4:
            option4()
        elif choice == 5:
            option5()
        elif choice == 6:
            option6()
        elif choice == 7:
            option7()
        elif choice == 8:
            option8()
        elif choice == 9:
            option9()
        elif choice == 10:
            click.echo("Exiting Source-Open. Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please select a valid option.\n")


if __name__ == "__main__":
    main()
