path = "./extraData/productData/"
# get all files
files = os.listdir(path)
products = []
for dataFile in files:
    data = json.load(open(path + dataFile))
    catLink = dataFile.split("_")[0] if len(dataFile.split("_")) > 1 else dataFile.split(".")[0]
    subLink = dataFile.split("_")[1].split(".")[0].split("_")[0] if len(dataFile.split("_")) > 1 else ""
    category = Category.objects.filter(link=catLink).first()
    if subLink != "":
        subcategory = SubCategory.objects.filter(link=subLink).first()
    for productData in data:
        try:
            newProduct = Product()
            newProduct.name = productData["attributes"]["name"]
            newProduct.category = category
            if subLink != "":
                newProduct.subcategory = subcategory
            newProduct.link = productData["id"]
            newProduct.product_label = productData["attributes"]["product_label"]
            newProduct.product_description = {}
            newProduct.varients = productData["attributes"]["facets"]
            newProduct.image_url = productData["attributes"]["image_url"]
            newProduct.image_urls = productData["attributes"]["image_urls"]
            newProduct.cashback_url = productData["attributes"]["cashback_url"]
            newProduct.is_compared = productData["attributes"]["is_compared"]
            newProduct.brand = productData["attributes"]["brand"]
            newProduct.offer_type = productData["attributes"]["offer_type"]
            newProduct.basePrice = productData["attributes"]["price"]
            newProduct.merchant = Merchant.objects.filter(name=productData["attributes"]["merchant_name"]).first()
            # newProduct.save()
            products.append(newProduct)
            print("Product Added: ", newProduct.name)
        except Exception as e:
            print("Error: ", e)
Product.objects.bulk_create(products)
