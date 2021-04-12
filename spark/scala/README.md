# Projetos com Scala


build.sbt
```
name := "ScalaSparkHelloWorld"

version := "0.1"

scalaVersion := "2.11.12"

// https://mvnrepository.com/artifact/org.apache.spark/spark-core
libraryDependencies += "org.apache.spark" %% "spark-core" % "2.4.7"
```

scala script
```scala
import org.apache.spark.{SparkConf, SparkContext}

object FirstSalaApplication {
  def main(args: Array[String]): Unit = {
    val conf =  new SparkConf()
    conf.setMaster("local")
    conf.setAppName("FirstApp")

    val sc = new SparkContext(conf)
    sc.setLogLevel("ERROR")

    //pi
    val NUM_SAMPLES = 100
    val count = sc.parallelize(1 to NUM_SAMPLES).filter { _ =>
      val x = math.random
      val y = math.random
      x*x + y*y < 1
    }.count()
    println(s"Pi is roughly ${4.0 * count / NUM_SAMPLES}")

  }
}
```