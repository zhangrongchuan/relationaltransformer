Can we use the primary–foreign key links, schema structure, and historical labels already available in relational databases to train a smaller model that directly performs entity classification on databases unseen during training, without retraining or fine-tuning on those target databases?


Existing GNNs for relational databases use primary–foreign key links for prediction, but typically require training for each database or task, limiting direct transfer to unseen databases.

Relational Transformers enable cross-database transfer, but use relatively large models to capture interactions between individual cells.

We argue that explicit database structure and historical labels provide strong priors: entity prediction can be organized around rows and their related records, reducing the interactions the model needs to learn.

This motivates our question: can shared row-level computation adapt to different database schemas and enable direct prediction on unseen databases with a substantially smaller model?