from Product import Product, redis
import time

key = "order_completed"
group='inventory-group'

try:
    redis.xgroup_create(key,group)
except: 
    print('group already exists')


while True:
    try:
        results= redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                product = Product.get(obj['product_id'])

                if product:
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                else:
                    redis.xadd('refund_order', obj,'*')
    except Exception as e:
        print(e)
    time.sleep(1)

    


