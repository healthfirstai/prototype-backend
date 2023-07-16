# NOTE: This is an example of prompt templates for our langchain agents
from langchain.output_parsers.list import CommaSeparatedListOutputParser
from langchain.prompts.prompt import PromptTemplate

# SQL Chain Prompt Template
CHAIN_PROMPT_SUFFIX = """Only use the following tables:
{table_info}

Question: {input}"""

CHAIN_INTERACTIVE_PROMPT_SUFFIX = """Only use the following tables:
{table_info}

Question: {input}
OriginalSQLQuery: {sql_input}
"""

# TODO: Change the unrelated user input to not use {use_input}
EXAMPLES_TEMPLATE = """
Reference Example:

Question: {user_input}
SQLQuery: {sql_query}

Unrelated user input example:

Question: {user_input}
SQLQuery:"""

SQL_CHAIN_INTERACTIVE_PREFIX = """You are a MySQL expert. Given a user input and original SQL query, modify the original SQL query according to the user input to create a syntactically correct MySQL query to run.
You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Importantly, if the user input does not seem related to the provided database tables, return an empty string as the Modified SQL query.

Use the following format:

Question: Question here
OriginalSQLQuery: Original SQL Query to modify
ModifiedSQLQuery: Modified SQL Query to run
"""

SQL_CHAIN_PREFIX = """You are a MySQL expert. Given a user input, create a syntactically correct MySQL query to run.
You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Importantly, if the user input does not seem related to the database tables, return an empty string as the SQL query.

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
"""

CHAIN_PROMPT_PREFIX = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

If the question does not seem related to the database tables, return an empty string as the answer.

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

"""

# Decider Prompt
_DECIDER_TEMPLATE = """Given the below input question and list of potential tables, output a comma separated list of the table names that may be necessary to answer this question.

Question: {query}

Table Names: {table_names}

Relevant Table Names:"""
DECIDER_PROMPT = PromptTemplate(
    input_variables=["query", "table_names"],
    template=_DECIDER_TEMPLATE,
    output_parser=CommaSeparatedListOutputParser(),
)

# SQL Agent Prompt Template
SQL_PREFIX = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then
look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always
limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples
in the database.
Never query for all the columns from a specific table, only ask for the relevant columns
given the question. You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to
construct your final answer.
You MUST double check your query before executing it.
If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database,
just return "I don't know" as the answer.
"""

FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""

SQL_SUFFIX = """Begin!

Question: {input}
Thought: I should look at the tables in the database to see what I can query.
{agent_scratchpad}"""

TABLE_INFO = {
    "lens_follow_view": """
        CREATE TABLE
          lens_follow_view (
            follower_id BIGINT,
            follower_address VARCHAR(255),
            follower VARCHAR(255),
            followee_id BIGINT,
            followee_address VARCHAR(255),
            followee VARCHAR(255),
            create_date DATE
          )
          /*
          3 rows from lens_follow_view table:
          follower_id     follower_address        follower        followee_id     followee_address        followee        create_date
          None    0x664ac330f874f3768e93c8511479de507eac649e      None    None    None    None    2022-05-27
          None    0x664ac330f874f3768e93c8511479de507eac649e      None    None    None    None    2022-05-27
          None    0x664ac330f874f3768e93c8511479de507eac649e      None    None    None    None    2022-06-03
          */
        """,
    "lens_profile_view": """
        CREATE TABLE
          lens_profile_view (
            `profileId` BIGINT,
            metadata TEXT,
            handle VARCHAR(255),
            address VARCHAR(255),
            `imageURI` TEXT,
            create_date DATE
          )
          /*
          3 rows from lens_profile_view table:
          profileId       metadata        handle  address imageURI        create_date
          498     https://arweave.net/_DtwFSb9FbbidrQk5uPIzih9dhbwDyCbzPmv5B8t2JM nandy.lens      0x005f16f017aa933bb41965b52848ceb8ee48b171      https://ipfs.infura.io/ipfs/QmRnnZAE3bt7BwpagGUxCrjBedE2HSByPCMJtexasLmjTA      2022-05-18
          1288    https://arweave.net/jHJll-m15hr1-WhE897yv517Io_6azuPwFsWGzSARdY sfyn_25.lens    0x00a722202e1a39363fd3a9b444cb5d225ff06d7c      https://ipfs.infura.io/ipfs/QmYvKvWgtENHv6PgoFRQraJrpUErV9EDcdjv3zNQ4hqFCU      2022-05-18
          438     https://arweave.net/0rQPizWpgfB6uCpsUVXY-XVolV214TLAEsB7-TCJgyE vietthu_95.lens 0x0184184dcebddc6342887260a643b72947c2d7e3      ipfs://bafybeiaa2ulsjlhhcsqhusvlksnrht5ur2fsrfzi2snz653vlx3wxeqlgq      2022-05-18
          */
        """,
    "lens_publication_comment_view": """
        CREATE TABLE
          lens_publication_comment_view (
            `profileId` BIGINT,
            address VARCHAR(255),
            handle VARCHAR(255),
            `pubId` INTEGER,
            `rootProfileId` BIGINT,
            `rootPubId` INTEGER,
            `contentURI` TEXT,
            `rootAddress` VARCHAR(255),
            `rootHandle` VARCHAR(255),
            TYPE VARCHAR(255),
            create_date DATE
          )
          /*
          3 rows from lens_publication_comment_view table:
          profileId       address handle  pubId   rootProfileId   rootPubId       contentURI      rootAddress     rootHandle      type    create_date
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    3       666     7       https://ipfs.infura.io/ipfs/QmcyVfgywoVVo1yzNUGippqWL6hfYvtSB33dxhHwWztxGg      None    None    Comment 2022-05-18
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    4       528     1       https://ipfs.infura.io/ipfs/QmcmY9iwcUMUKjbnYS41Phs3YWCDe9akXbDEfWSedtdFtY      0xa83444576f86c8b59a542ec2f286a19ab12c2666      paris.lens      Comment 2022-05-18
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    6       2545    1       https://ipfs.infura.io/ipfs/QmUqD2ZGJjaCKvM46RSJU6RcpWPKqYNTcR7UdMvmYnHLwa      None    None    Comment 2022-05-18
          */

        """,
    "lens_publication_mirror_view": """
        CREATE TABLE
          lens_publication_mirror_view (
            `profileId` BIGINT,
            address VARCHAR(255),
            handle VARCHAR(255),
            `pubId` INTEGER,
            `rootProfileId` BIGINT,
            `rootPubId` INTEGER,
            `contentURI` TEXT,
            `rootAddress` VARCHAR(255),
            `rootHandle` VARCHAR(255),
            TYPE VARCHAR(255),
            create_date DATE
          )
          /*
          3 rows from lens_publication_mirror_view table:
          profileId       address handle  pubId   rootProfileId   rootPubId       contentURI      rootAddress     rootHandle      type    create_date
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    5       13      1       None    None    None    Mirror  2022-05-18
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    19      10402   1       None    None    None    Mirror  2022-05-25
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    60      7193    55      None    None    None    Mirror  2022-06-07
          */

        """,
    "lens_publication_post_view": """
        CREATE TABLE
          lens_publication_post_view (
            `profileId` BIGINT,
            address VARCHAR(255),
            handle VARCHAR(255),
            `pubId` INTEGER,
            `rootProfileId` BIGINT,
            `rootPubId` INTEGER,
            `contentURI` TEXT,
            `rootAddress` VARCHAR(255),
            `rootHandle` VARCHAR(255),
            TYPE VARCHAR(255),
            create_date DATE
          )
          /*
          3 rows from lens_publication_post_view table:
          profileId       address handle  pubId   rootProfileId   rootPubId       contentURI      rootAddress     rootHandle      type    create_date
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    1       None    None    https://ipfs.infura.io/ipfs/QmPxtCahfVLpsEp5HnMCUHMovx5wELH1p8X4ZMTgF6iEue      None    None    Post    2022-05-18
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    2       None    None    https://ipfs.infura.io/ipfs/QmQhFyBjjLJcdta7CMzjCkSp18qAQsTBKh8bWhnkZtEi92      None    None    Post    2022-05-18
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    10      None    None    https://ipfs.infura.io/ipfs/QmeWhzM7fTJLzkfKinyC3ZyZKurfBSvuEBsoPWekbRDxX1      None    None    Post    2022-05-19
          */

        """,
    "lens_publication_view": """
        CREATE TABLE
          lens_publication_view (
            `profileId` BIGINT,
            address VARCHAR(255),
            handle VARCHAR(255),
            `rootProfileId` BIGINT,
            `rootPubId` INTEGER,
            `pubId` INTEGER,
            `contentURI` TEXT,
            `rootAddress` VARCHAR(255),
            `rootHandle` VARCHAR(255),
            TYPE VARCHAR(255),
            create_date DATE
          )
          /*
          3 rows from lens_publication_view table:
          profileId       address handle  rootProfileId   rootPubId       pubId   contentURI      rootAddress     rootHandle      type    create_date
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    None    None    1       https://ipfs.infura.io/ipfs/QmPxtCahfVLpsEp5HnMCUHMovx5wELH1p8X4ZMTgF6iEue      None    None    Post    2022-05-18
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    None    None    2       https://ipfs.infura.io/ipfs/QmQhFyBjjLJcdta7CMzjCkSp18qAQsTBKh8bWhnkZtEi92      None    None    Post    2022-05-18
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    666     7       3       https://ipfs.infura.io/ipfs/QmcyVfgywoVVo1yzNUGippqWL6hfYvtSB33dxhHwWztxGg      None    None    Comment 2022-05-18
          */
        """,
    "lens_publication_summary_view": """
        CREATE TABLE
          lens_publication_summary_view (
            profile_id BIGINT,
            address VARCHAR(255),
            handle VARCHAR(255),
            in_reply_to_profile_id BIGINT,
            in_reply_to_pub_id INTEGER,
            pub_id INTEGER,
            `content_URI` TEXT,
            in_reply_to_address VARCHAR(255),
            in_reply_to_handle VARCHAR(255),
            create_date DATE,
            TYPE VARCHAR(255),
            comment_count BIGINT DEFAULT '0',
            mirror_count BIGINT DEFAULT '0',
            image VARCHAR(255),
            `imageMimeType` VARCHAR(255)
          )
          /*
          3 rows from lens_publication_summary_view table:
          profile_id      address handle  in_reply_to_profile_id  in_reply_to_pub_id      pub_id  content_URI     in_reply_to_address     in_reply_to_handle      create_date     type    comment_count   mirror_count    image   imageMimeType
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    None    None    1       https://ipfs.infura.io/ipfs/QmPxtCahfVLpsEp5HnMCUHMovx5wELH1p8X4ZMTgF6iEue      None    None    2022-05-18      Post    None    None    None    None
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    None    None    2       https://ipfs.infura.io/ipfs/QmQhFyBjjLJcdta7CMzjCkSp18qAQsTBKh8bWhnkZtEi92      None    None    2022-05-18      Post    None    None    None    None
          5       0x7241dddec3a6af367882eaf9651b87e1c7549dff      None    666     7       3       https://ipfs.infura.io/ipfs/QmcyVfgywoVVo1yzNUGippqWL6hfYvtSB33dxhHwWztxGg      None    None    2022-05-18      Comment None    None    None    None
          */

        """,
    "vote": """
        CREATE TABLE
          vote (
            id VARCHAR(255) COLLATE utf8mb3_bin NOT NULL,
            voter VARCHAR(255) COLLATE utf8mb3_bin COMMENT 'æŠ•ç¥¨è€…(åœ°å€)',
            choice INTEGER COMMENT 'ææ¡ˆä¸­çš„é€‰é¡¹',
            `spaceId` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
            `spaceName` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
            `spaceAvatar` VARCHAR(255) COLLATE utf8mb3_bin,
            `spaceAdmins` JSON COMMENT 'spaceç®¡ç†å‘˜',
            `spaceModerators` JSON,
            `spaceMembers` JSON,
            `proposalId` VARCHAR(255) COLLATE utf8mb3_bin,
            `proposalAuthor` VARCHAR(255) COLLATE utf8mb3_bin COMMENT 'ææ¡ˆä½œè€…',
            `proposalTitle` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
            created TIMESTAMP NULL
          ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb3
          /*
          3 rows from vote table:
          id      voter   choice  spaceId spaceName       spaceAvatar     spaceAdmins     spaceModerators spaceMembers    proposalId      proposalAuthor  proposalTitle   created
          0x12745be33398bc8d8a6d764d0903779159b8007ec7878cde17a2472539b67306      0xb8ff2304e7ac275a43cc4dee3d7380d761dd52a9      3       ppyaa.eth       paopao  ipfs://QmVsj2H5pf3M72Qi9bTJXV58CKurhUSpLbtumZ1WrH5pE1   ['0x6ceea0fc41387fc6780aa78125ffde3ece0dc103']  []      ['0x6ceea0fc41387fc6780aa78125ffde3ece0dc103']  0xdbe249a27c1531e47e5ab7dd38b12cd3230f800f4ade79799b7c35ae0760ca04     0x6ceea0fc41387fc6780aa78125ffde3ece0dc103      Favorite evm development tools  2021-11-20 17:45:15
          0x2358121e20703a766d70ac22b8f73bf3288f528becd6c75a4c438ac8a285fd3e      0xc3e971015554a296e9c55a9d0d8a180dc5f05c5b      3       ppyaa.eth       paopao  ipfs://QmVsj2H5pf3M72Qi9bTJXV58CKurhUSpLbtumZ1WrH5pE1   ['0x6ceea0fc41387fc6780aa78125ffde3ece0dc103']  []      ['0x6ceea0fc41387fc6780aa78125ffde3ece0dc103']  0xdbe249a27c1531e47e5ab7dd38b12cd3230f800f4ade79799b7c35ae0760ca04     0x6ceea0fc41387fc6780aa78125ffde3ece0dc103      Favorite evm development tools  2021-11-20 17:45:17
          0xe7c106005e3650696df133aaf73b6654a662f5e2bbf6c0e5335247303acd9dae      0x16878f996f6283a9d8838216e7aa3c410844b492      1       ppyaa.eth       paopao  ipfs://QmVsj2H5pf3M72Qi9bTJXV58CKurhUSpLbtumZ1WrH5pE1   ['0x6ceea0fc41387fc6780aa78125ffde3ece0dc103']  []      ['0x6ceea0fc41387fc6780aa78125ffde3ece0dc103']  0xdbe249a27c1531e47e5ab7dd38b12cd3230f800f4ade79799b7c35ae0760ca04     0x6ceea0fc41387fc6780aa78125ffde3ece0dc103      Favorite evm development tools  2021-11-20 17:45:19
          */
        """,
    "lens_overall_level_view": """
        CREATE TABLE
          lens_overall_level_view (
            `profileId` VARCHAR(200),
            handle VARCHAR(255),
            create_date VARCHAR(10),
            overall_level_str VARCHAR(10),
            overall_level BIGINT,
            overall_level_rank BIGINT,
            overall_level_score DOUBLE,
            address VARCHAR(200),
            influ_level BIGINT,
            influ_level_str VARCHAR(10),
            compaign_level BIGINT,
            engager_level BIGINT,
            compaign_level_str VARCHAR(10),
            engager_level_str VARCHAR(10),
            creator_level BIGINT,
            creator_level_str VARCHAR(10),
            collector_level BIGINT,
            collector_level_str VARCHAR(10),
            curator_level BIGINT,
            curator_level_str VARCHAR(10)
          )
          /*
          3 rows from lens_overall_level_view table:
          profileId       handle  create_date     overall_level_str       overall_level   overall_level_rank      overall_level_score     address influ_level     influ_level_str compaign_level  engager_level   compaign_level_str      engager_level_str       creator_level   creator_level_str       collector_level collector_level_str    curator_level   curator_level_str
          
          */
        """,
    "lens_overall_score_view": """
        CREATE TABLE
          lens_overall_score_view (
            `profileId` VARCHAR(200),
            handle VARCHAR(255),
            address VARCHAR(200),
            pr_value_influ DOUBLE,
            pr_score_influ DOUBLE,
            pr_rank_influ BIGINT,
            pr_value_comment_compaign DOUBLE,
            pr_score_comment_compaign DOUBLE,
            pr_rank_comment_compaign BIGINT,
            pr_value_mirror_compaign DOUBLE,
            pr_score_mirror_compaign DOUBLE,
            pr_rank_mirror_compaign BIGINT,
            pr_score_compaign DOUBLE,
            pr_rank_compaign BIGINT,
            pr_value_comment_engager DOUBLE,
            pr_score_comment_engager DOUBLE,
            pr_rank_comment_engager BIGINT,
            pr_value_mirror_engager DOUBLE,
            pr_score_mirror_engager DOUBLE,
            pr_rank_mirror_engager BIGINT,
            pr_score_engager DOUBLE,
            pr_rank_engager BIGINT,
            pr_value_creator DOUBLE,
            pr_score_creator DOUBLE,
            pr_rank_creator BIGINT,
            pr_value_collector DOUBLE,
            pr_score_collector DOUBLE,
            pr_rank_collector BIGINT,
            curator_score BIGINT,
            curator_rank BIGINT,
            overall_score DOUBLE,
            overall_rank BIGINT,
            create_date VARCHAR(10)
          )
          /*
          3 rows from lens_overall_score_view table:
          profileId       handle  address pr_value_influ  pr_score_influ  pr_rank_influ   pr_value_comment_compaign       pr_score_comment_compaign       pr_rank_comment_compaign        pr_value_mirror_compaign        pr_score_mirror_compaign        pr_rank_mirror_compaign pr_score_compaign       pr_rank_compaign        pr_value_comment_engager       pr_score_comment_engager        pr_rank_comment_engager pr_value_mirror_engager pr_score_mirror_engager pr_rank_mirror_engager  pr_score_engager        pr_rank_engager pr_value_creator        pr_score_creator        pr_rank_creator pr_value_collector      pr_score_collector      pr_rank_collector      curator_score   curator_rank    overall_score   overall_rank    create_date
          
          */
        """,
}
