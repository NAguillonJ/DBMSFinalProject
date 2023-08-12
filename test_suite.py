import time
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


# create a function to send any query to the database
def sendQuery(query):
    cursor.execute(query)
    for row in cursor.fetchall():
        click.echo(row)
    click.echo("\n")


def option1_tester():
    start_time = time.time()
    type_ = 'primary'
    print("Testing Option 1")
    result = 
    print(f"Expected Result %s", result)
    # create query based on stored procdure findClaimsByType
    cursor.callproc("FindClaimsByType", [type_])
    for result in cursor.stored_results():
        for row in result.fetchall():
            click.echo(row[3])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 1 testing... took %f seconds", elapsed_time)


def option2_tester():
    start_time = time.time()
    claim_type = 'primary'
    count = 800
    print("Testing Option 2")
    # create query based on stored procdure findClaimsByTypeCitedMoreThan
    cursor.callproc("FindClaimsByTypeCitedMoreThan", [claim_type, count])
    for result in cursor.stored_results():
        for row in result.fetchall():
            if row[3] == 
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 2 testing... took %f seconds", elapsed_time)


def option3_tester():
    print("Testing Option 3")
    start_time = time.time()
    keyword = click.prompt("Enter the keyword:", type=str)
    # create query based on stored procdure findArticlesWithKeywordInHeadline
    cursor.callproc("FindArticlesWithKeywordInHeadline", [keyword])
    for result in cursor.stored_results():
        for row in result.fetchall():
            click.echo(row[0])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 3 testing... took %f seconds", elapsed_time)
    click.echo("\n")


def option4_tester():
    print("Testing Option 4")
    start_time = time.time()
    author = click.prompt("Enter the author:", type=str)
    # create regular query
    cursor.execute(
        "SELECT AD.Headline, A.URL FROM Article AS A, ArticleDetails AS AD, WrittenBy AS WB, Author AS AT WHERE AD.URL = A.URL AND A.ArticleID = WB.ArticleID AND WB.AuthorID = AT.AuthorID AND AT.AuthorName  = '%s';",
        (author, ))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 4 testing... took %f seconds", elapsed_time)


def option5_tester():
    print("Testing Option 5")
    start_time = time.time()
    publisher = click.prompt("Enter the publisher:", type=str)
    start = click.prompt("Enter the start date:", type=str)
    end = click.prompt("Enter the end date:", type=str)
    # create query
    cursor.execute(
        "SELECT AD.Headline, A.URL FROM Article AS A, ArticleDetails AS AD WHERE AD.URL = A.URL AND AD.PubName = P.PubName AND AD.PubName = '%s' AND A.DatePublished BETWEEN '%s' AND '%s' ORDER BY A.DatePublished;",
        (publisher, start, end))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 5 testing... took %f seconds", elapsed_time)


def option6_tester():
    print("Testing Option 6")
    start_time = time.time()
    count = click.prompt("Enter the lower bound:", type=int)
    # create query
    cursor.execute(
        "SELECT AT.AuthorName FROM Author AS AT, WrittenBy AS WB, Claim AS C, CollectionOf AS CO WHERE AT.AuthorID = WB.AuthorID AND WB.ArticleID = CO.ArticleID AND CO.ClaimID = C.ClaimID GROUP BY AT.AuthorName HAVING COUNT(C.numCitations) > %s;",
        (count, ))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 7 testing... took %f seconds", elapsed_time)


def option7_tester():
    print("Testing Option 7")
    start_time = time.time()
    type = click.prompt("Enter the type of claim:", type=str)
    # create query
    cursor.execute(
        "SELECT AD.Headline, A.URL FROM Article AS A, ArticleDetails AS AD, CollectionOf AS CO, Claim AS C WHERE AD.URL = A.URL AND A.ArticleID = CO.ArticleID AND CO.ClaimID = C.ClaimID AND C.ClaimType = '%s';",
        (type, ))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 7 testing... took %f seconds", elapsed_time)


def option8_tester():
    print("Testing Option 8")
    start_time = time.time()
    author = click.prompt("Enter the author:", type=str)
    # create query
    cursor.execute(
        "SELECT C.ClaimType, AD.Headline FROM Article AS A, ArticleDetails AS AD, CollectionOf AS CO, Claim AS C, WrittenBy AS WB, Author AS AT WHERE AD.URL = A.URL AND A.ArticleID = CO.ArticleID AND CO.ClaimID = C.ClaimID AND A.ArticleID = WB.ArticleID AND WB.AuthorID = AT.AuthorID AND AT.AuthorName = '%s';",
        (author, ))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 8 testing... took %f seconds", elapsed_time)


def option9_tester():
    print("Testing Option 9")
    start_time = time.time()
    count = click.prompt("Enter the lower bound:", type=int)
    start = click.prompt("Enter the start date:", type=str)
    end = click.prompt("Enter the end date:", type=str)
    author = click.prompt("Enter the author:", type=str)
    # create query
    cursor.execute(
        "SELECT AD.Headline FROM Article AS A, ArticleDetails AS AD, CollectionOf AS CO, Claim AS C, WrittenBy AS WB, Author AS AT WHERE AD.URL = A.URL AND A.ArticleID = CO.ArticleID AND CO.ClaimID = C.ClaimID AND A.ArticleID = WB.ArticleID AND WB.AuthorID = AT.AuthorID AND AT.AuthorName = '%s' AND C.ClaimType = 'Tertiary' AND C.numCitations > %s AND A.DatePublished BETWEEN '%s' AND '%s';",
        (author, count, start, end))
    for row in cursor.fetchall():
        click.echo(row[0])
    click.echo("\n")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 9 testing... took %f seconds", elapsed_time)


def test_suite():
    print("Testing!")
    start_time = time.time()
    option1_tester()
    option2_tester()
    option3_tester()
    option4_tester()
    option5_tester()
    option6_tester()
    option7_tester()
    option8_tester()
    option9_tester()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Testing... took a total of  %f seconds", elapsed_time)

def main():
    print("Launching Test Suite")
    test_suite()
    


if __name__ == "__main__":
    main()
