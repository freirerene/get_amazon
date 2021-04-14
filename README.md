# Get Amazon Infos

In this project we create a script that monitors some features of products (we simply put the link to the product on `products.csv`) from Amazon.com: price, rating, weight, volume, etc.

We store these information on a SQL database: one table `product` stores the name, price and when the info was collected. The table `characteristics` stores the manufacturer, brand, weight, volume and rating. One table is connected to the other via an Id.

The way we use this script is by hosting it on a VM on google cloud and running a cron job to collect data every day. This way we have some nice time series on the features of the products we want.
