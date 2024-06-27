files = os.listdir(path)
for dataFile in files:
    data = json.load(open(path + dataFile))
    for product in data:
        try:
            for merchant in product["relationships"]["products_compared"]:
                store = Store.objects.filter(name=merchant["attributes"]["merchant"]["report_storename"]).first()
                newMerchant = Merchant()
                newMerchant.name = merchant["attributes"]["merchant"]["name"]
                newMerchant.link = merchant["attributes"]["merchant"]["unique_identifier"]
                newMerchant.store = store
                newMerchant.save()
                print(newMerchant.name)
        except:
            pass
