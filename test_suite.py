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
    expectedAnswer = 42
    # create query based on stored procdure findClaimsByType
    cursor.callproc("FindClaimsByType", [type_])
    actualAnswer = 0
    for result in cursor.stored_results():
        for row in result.fetchall():
            actualAnswer+=1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 1 testing... took {elapsed_time} seconds")
    print(f"Expected Result {expectedAnswer}")
    print(f"Actual Result {actualAnswer}")
    print("\n")

def option2_tester():
    start_time = time.time()
    claim_type = 'secondary'
    count = 650 # rank 3
    print("Testing Option 2")
    expectedAnswer = 31
    actualAnswer = 0
    # create query based on stored procdure FindClaimsByTypeAndCitations
    cursor.callproc("FindClaimsByTypeAndCitations", [claim_type, count])
    for result in cursor.stored_results():
        for row in result.fetchall():
            actualAnswer = row[0]
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 2 testing... took {elapsed_time} seconds")
    print(f"Expected Result {expectedAnswer}")
    print(f"Actual Result {actualAnswer}")
    print("\n")


def option3_tester():
    print("Testing Option 3")
    start_time = time.time()
    keyword = 'America'
    expectedAnswer = 4
    actualAnswer = 0
    # create query based on stored procdure FindArticlesByKeyword
    cursor.callproc("FindArticlesByKeyword", [keyword])
    for result in cursor.stored_results():
        for row in result.fetchall():
            actualAnswer += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 3 testing... took {elapsed_time} seconds")
    print(f"Expected Result {expectedAnswer}")
    print(f"Actual Result {actualAnswer}")
    print("\n")


def option4_tester():
    print("Testing Option 4")
    start_time = time.time()
    author = 'Susan Davis'
    #click.prompt("Enter the author", type=str)
    # create regular query
    expectedAnswer = 1
    actualAnswer = 0
    cursor.execute(
        """SELECT AD.Headline, A.URL 
        FROM Article AS A, ArticleDetails AS AD, WrittenBy AS WB, Author AS AT 
        WHERE AD.URL = A.URL 
            AND A.ArticleID = WB.ArticleID 
            AND WB.AuthorID = AT.AuthorID 
            AND AT.AuthorName  = %s;""",
            (author,))
    for row in cursor.fetchall():
        actualAnswer+=1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 4 testing... took {elapsed_time} seconds")
    print(f"Expected Result {expectedAnswer}")
    print(f"Actual Result {actualAnswer}")
    print("\n")


def option5_tester():
    print("Testing Option 5")
    start_time = time.time()
    publisher = 'NPR' #click.prompt("Enter the publisher", type=str)
    start = '2016-01-01' #click.prompt("Enter the start date", type=str)
    end = '2016-10-01' #click.prompt("Enter the end date", type=str)
    expectedAnswer = 4
    actualAnswer = 0
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
        actualAnswer+=1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 5 testing... took {elapsed_time} seconds")
    print(f"Expected Result {expectedAnswer}")
    print(f"Actual Result {actualAnswer}")
    print("\n")


def option6_tester():
    print("Testing Option 6")
    start_time = time.time()
    count = 10 # Band 1 # click.prompt("Enter the band(1 - 5)", type=int)
    expectedAnswer = 2
    actualAnswer = 0
    # create query
    cursor.execute("""
                   SELECT AT.AuthorName 
                   FROM Author AS AT, WrittenBy AS WB, Claim AS C, CollectionOf AS CO 
                   WHERE AT.AuthorID = WB.AuthorID 
                        AND WB.ArticleID = CO.ArticleID 
                        AND CO.ClaimID = C.ClaimID 
                        GROUP BY AT.AuthorName 
                        HAVING COUNT(C.numCitations) > %s;""", 
                    (count,))
    for row in cursor.fetchall():
        actualAnswer+=1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 6 testing... took {elapsed_time} seconds")
    print(f"Expected Result {expectedAnswer}")
    print(f"Actual Result {actualAnswer}")
    print("\n")


def option7_tester():
    print("Testing Option 7")
    start_time = time.time()
    type = 'primary' #click.prompt("Enter the type of claim:", type=str)
    expectedAnswer = 18
    actualAnswer = 0
    # create query
    cursor.execute("""
                   SELECT DISTINCT AD.Headline, A.URL 
                   FROM Article AS A, ArticleDetails AS AD, CollectionOf AS CO, Claim AS C 
                   WHERE AD.URL = A.URL 
                        AND A.ArticleID = CO.ArticleID 
                        AND CO.ClaimID = C.ClaimID 
                        AND C.type = %s;""",
        (type, ))
    for row in cursor.fetchall():
        actualAnswer += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 7 testing... took {elapsed_time} seconds")
    print(f"Expected Result {expectedAnswer}")
    print(f"Actual Result {actualAnswer}")
    print("\n")


def option8_tester():
    print("Testing Option 8")
    start_time = time.time()
    author = 'Michelle Nichols' #click.prompt("Enter the author:", type=str)
    expectedAnswer = 4
    actualAnswer = 0
    # create query
    cursor.execute("""
                   SELECT C.type, AD.Headline FROM Article AS A, ArticleDetails AS AD, CollectionOf AS CO, Claim AS C, WrittenBy AS WB, Author AS AT 
                   WHERE AD.URL = A.URL 
                        AND A.ArticleID = CO.ArticleID 
                        AND CO.ClaimID = C.ClaimID 
                        AND A.ArticleID = WB.ArticleID 
                        AND WB.AuthorID = AT.AuthorID 
                        AND AT.AuthorName LIKE %s;""",
        (author, ))
    for row in cursor.fetchall():
        actualAnswer+=1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 8 testing... took {elapsed_time} seconds")
    print(f"Expected Result {expectedAnswer}")
    print(f"Actual Result {actualAnswer}")
    print("\n")


def option9_tester():
    print("Testing Option 9")
    start_time = time.time()
    count = 650 #click.prompt("Enter the lower bound:", type=int)
    start = 2016-1-1 #click.prompt("Enter the start date:", type=str)
    end = 2017-12-31 #click.prompt("Enter the end date:", type=str)
    author = 'Michelle Nichols' #click.prompt("Enter the author:", type=str)
    expectedAnswer = 0
    actualAnswer = 0
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
        click.echo(row[0] + "\n")
        actualAnswer += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query 9 testing... took {elapsed_time} seconds")
    print(f"Expected Result {expectedAnswer}")
    print(f"Actual Result {actualAnswer}")
    print("\n")


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
