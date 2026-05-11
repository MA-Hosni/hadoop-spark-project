from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
import logging

# Setup logging so you can see progress
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def clean_games_table(games_df: DataFrame) -> DataFrame:
    """
    Clean games info table: normalized Rating column
    E -> Everyone, T -> Teen, M -> Mature
    """
    games_df = games_df.dropDuplicates(['GameID'])
    
    # Replace single letters with full words
    games_df = games_df.withColumn(
        "Rating",
        F.when(F.col("Rating") == "E", "Everyone")
        .when(F.col("Rating") == "T", "Teen")
        .when(F.col("Rating") == "M", "Mature")
        .otherwise("NoRating"),
    )
    return games_df

def clean_activities_table(activities_df: DataFrame) -> DataFrame:
    """
    Clean activities table: 
    - Categorize Level into Beginner/Mid-Level/Advanced
    - Calculate session duration in minutes
    """
    # Categorize player levels
    activities_df = activities_df.withColumn(
        "Level",
        F.when(F.col("Level") < 30, "Beginner")
        .when((F.col("Level") >= 30) & (F.col("Level") < 60), "Mid-Level")
        .when(F.col("Level") >= 60, "Advanced")
        .otherwise("Unknown"),
    )
    
    # Convert to timestamp type
    activities_df = activities_df.withColumn(
        'StartTime', F.col('StartTime').cast('timestamp')
    )
    activities_df = activities_df.withColumn(
        'EndTime', F.col('EndTime').cast('timestamp')
    )
    
    # Calculate duration in minutes
    activities_df = activities_df.withColumn(
        'SessionDuration',
        (F.col('EndTime').cast('long') - F.col('StartTime').cast('long')) / 60,
    )
    
    return activities_df

def session_metrics(activites_df: DataFrame) -> DataFrame:
    """
    KPI 1: Overall session statistics
    Average session duration, XP earned, quests completed, etc.
    """
    session_metrics_df = activites_df.select(
        F.round(F.mean(F.col("SessionDuration"))).alias("Avg_SessionDuration_minutes"),
        F.round(F.mean(F.col("ExperiencePoints"))).alias("Avg_ExperiencePoints"),
        F.round(F.mean(F.col("AchievementsUnlocked"))).alias("Avg_AchievementsUnlocked"),
        F.round(F.mean(F.col("CurrencyEarned"))).alias("Avg_CurrencyEarned"),
        F.round(F.mean(F.col("CurrencySpent"))).alias("Avg_CurrencySpent"),
        F.round(F.mean(F.col("QuestsCompleted"))).alias("Avg_QuestsCompleted"),
    ).orderBy(F.col('Avg_SessionDuration_minutes').desc())
    
    return session_metrics_df

def game_genre_metrics(activities_df: DataFrame, games_df: DataFrame) -> DataFrame:
    """
    KPI 2: Metrics by game genre
    Join player activity with game info, then group by genre
    """
    game_genre_metrics_df = (
        activities_df.join(games_df, on='GameID', how='inner')
        .groupBy('Genre')
        .agg(
            F.round(F.mean(F.col("SessionDuration"))).alias("Avg_SessionDuration_minutes"),
            F.sum(F.col("QuestsCompleted")).alias("Total_QuestsCompleted"),
            F.round(F.mean(F.col("Game_Length"))).alias("Avg_Game_Length_minutes"),
        )
    )
    return game_genre_metrics_df

def player_level_metrics(activities_df: DataFrame) -> DataFrame:
    """
    KPI 3: Metrics by player skill level
    """
    player_lvl_metrics_df = activities_df.groupBy('Level').agg(
        F.round(F.mean(F.col("EnemiesDefeated"))).alias("Avg_EnemiesDefeated"),
        F.round(F.mean(F.col("QuestsCompleted"))).alias("Avg_QuestsCompleted"),
    )
    return player_lvl_metrics_df

def write_to_parquet(path: str, df: DataFrame):
    """
    Save results as Parquet format (compressed, columnar - very efficient!)
    """
    df.write.mode("overwrite").parquet(path, compression=None)
    logger.info(f"File {path} saved to HDFS!!")

def main():
    # Create Spark session - the entry point to all Spark functionality
    with SparkSession.builder.appName("spark_project").getOrCreate() as spark:
        
        # Read CSV files from HDFS
        games_df = spark.read.csv(
            "hdfs://namenode:9000/root/input/games_data.csv", 
            inferSchema=True, header=True
        )
        activities_df = spark.read.csv(
            "hdfs://namenode:9000/root/input/players_data.csv", 
            inferSchema=True, header=True
        )
        
        # Clean data
        games_clean_df = clean_games_table(games_df)
        activities_clean_df = clean_activities_table(activities_df)
        
        # Calculate KPIs
        session_metrics_df = session_metrics(activities_clean_df)
        game_genre_metrics_df = game_genre_metrics(activities_clean_df, games_clean_df)
        player_level_metrics_df = player_level_metrics(activities_clean_df)
        
        # Save results back to HDFS as Parquet
        write_to_parquet("hdfs://namenode:9000/root/sparkoutput/Session_metrics.parquet", session_metrics_df)
        write_to_parquet("hdfs://namenode:9000/root/sparkoutput/Games_genre_metrics.parquet", game_genre_metrics_df)
        write_to_parquet("hdfs://namenode:9000/root/sparkoutput/Player_level_metrics.parquet", player_level_metrics_df)

if __name__ == '__main__':
    main()
