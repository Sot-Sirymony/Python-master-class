

# main.py
import module_test.pricing as p
net_price = p.get_net_price(
price=100,
tax_rate=0.01
)
print(net_price)