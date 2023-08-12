import click
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="test_correctness",
    auth_plugin="mysql_native_password",
)

cursor = db.cursor()

# create a function to send any query to the database (for testing purposes)
def sendQuery(query):
    cursor.execute(query)
    for row in cursor.fetchall():
        click.echo(row)
    click.echo("\n")


def option1():
    type = click.prompt("Enter the type of claim", type=str)
    # create query based on stored procdure findClaimsByType
    cursor.callproc("FindClaimsByType", [type])
    count = 0
    for result in cursor.stored_results():
        for row in result.fetchall():
            count += 1
    click.echo("Number claims of type " + type + ": " + str(count)) 
    click.echo("-------------------------------------------\n")


def option2():
    # 5 star Authenticity >= 1000
    # 4 >= 875
    # 3 >= 650
    # 2 >= 325
    # 1 >= 125
    type = click.prompt("Enter the type of claim", type=str)
    count = click.prompt("Enter the authencity (1 - 5)", type=int)
    # create query based on stored procdure FindClaimsByTypeAndCitations
    authenticity = 0
    if count == 1:
        authenticity = 125
    elif count == 2:
        authenticity = 325
    elif count == 3:
        authenticity = 650
    elif count == 4:
        authenticity = 875
    elif count == 5:
        authenticity = 1000
    cursor.callproc("FindClaimsByTypeAndCitations", [type, authenticity])
    click.echo("All claims of type " + type + " with authenticity " + str(count) + ":\n")
    for result in cursor.stored_results():
        for row in result.fetchall():
            click.echo(row[0] + " " + row[1] + "\n")
    click.echo("-------------------------------------------\n")


def option3():
    keyword = click.prompt("Enter the keyword", type=str)
    # create query based on stored procdure findArticlesWithKeywordInHeadline
    cursor.callproc("FindArticlesByKeyword", [keyword])
    click.echo("All articles with keyword " + keyword + " in the headline:\n")
    for result in cursor.stored_results():
        for row in result.fetchall():
            click.echo(row[0] + "\n")
    click.echo("-------------------------------------------\n")


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
    click.echo("All articles by " + author + ":\n")
    for row in cursor.fetchall():
        click.echo(row[0] + "\n")
    click.echo("-------------------------------------------\n")

def option5():
    publisher = click.prompt("Enter the publisher", type=str)
    start = click.prompt("Enter the start date (YYYY - M - D)", type=str)
    end = click.prompt("Enter the end date (YYYY - M - D)", type=str)
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
    click.echo("All articles by " + publisher + " between " + start + " and " + end + ":\n")
    for row in cursor.fetchall():
        click.echo(row[0] + "\n")
    click.echo("-------------------------------------------\n")


def option6():
    #Band 5 >=500
    #4>=350
    #3>=100
    #2>=50
    #1>=10
    count = click.prompt("Enter band (1 - 5)", type=int)
    band  = 0
    if count == 1:
        band = 10
    elif count == 2:
        band = 50
    elif count == 3:
        band = 100
    elif count == 4:
        band = 350
    elif count == 5:
        band = 500
    # create query
    cursor.execute("""
                   SELECT AT.AuthorName 
                   FROM Author AS AT, WrittenBy AS WB, Claim AS C, CollectionOf AS CO 
                   WHERE AT.AuthorID = WB.AuthorID 
                        AND WB.ArticleID = CO.ArticleID 
                        AND CO.ClaimID = C.ClaimID 
                        GROUP BY AT.AuthorName 
                        HAVING COUNT(C.numCitations) > %s;""", (band,))
    click.echo("All authors in band " + str(count) + ":\n")
    for row in cursor.fetchall():
        click.echo(row[0] + "\n")
    click.echo("-------------------------------------------\n")

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
    click.echo("All articles with claim type " + type + ":\n")
    for row in cursor.fetchall():
        click.echo(row[0] + "\n")
    click.echo("-------------------------------------------\n")

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
                        AND AT.AuthorName LIKE %s;""",   (author,))
    click.echo("All articles by " + author + ":\n")
    for row in cursor.fetchall():
        click.echo(row[0]+ " - " + row[1]  + "\n")
    click.echo("-------------------------------------------\n")


def option9():
    band = click.prompt("Enter band (1 - 5)", type=int)
    start = click.prompt("Enter the start date", type=str)
    end = click.prompt("Enter the end date", type=str)
    author = click.prompt("Enter the author", type=str)
    # create query
    authenticity = 0
    if band == 1:
        authenticity = 125
    elif band == 2:
        authenticity = 325
    elif band == 3:
        authenticity = 650
    elif band == 4:
        authenticity = 875
    elif band == 5:
        authenticity = 1000
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
                        (author, authenticity, start, end))
    click.echo("All tertiary claims by " + author + " between " + start + " and " + end + " with authenticity higher than level " + str(band) + ":\n")
    for row in cursor.fetchall():
        click.echo(row[0] + "\n")
    click.echo("-------------------------------------------\n")

def main():
    click.echo("Welcome to SOURCE-OPEN!\n")

    while True:
        click.echo("Select an option:")
        click.echo("1. Show number of claims per type.")
        click.echo(
            "2. Filter by claim type and authenticity rank."
        )
        click.echo("3. Filter by keywords in Headline.")
        click.echo("4. Filter by author name.")
        click.echo(
            "5. Filter by publisher name and publication date range."
        )
        click.echo(
            "6. List authors by popularity band."
        )
        click.echo(
            "7. Filter article headlines and URLs by claim type. "
        )
        click.echo(
            "8. Filter article headlines by author name and sort by claim type."
        )
        click.echo(
            "9. Filter tertiary claims by author name, publication date range and authenticity rank."
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
