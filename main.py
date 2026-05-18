from src.pipelines.train_pipeline import TrainPipeline


def main():
    metrics = TrainPipeline().run()
    print(f"Training completed. Metrics: {metrics}")


if __name__ == "__main__":
    main()
