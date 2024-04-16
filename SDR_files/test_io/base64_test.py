import base64

# buff = b"Hello, World!"
# buff = b'95xaq1ymVbdklcnM1IntEdYHV8F35vP4rq+69b3vypPvWkDBPfJIB2PeICk9iAPvkbjugpaPEFZv573vZQDu5Q=='
buff = b'\xf7\x9cZ\xab\\\xa6U\xb7d\x95\xc9\xcc\xd4\x89\xed\x11\xd6\x07W\xc1w\xe6\xf3\xf8\xae\xaf\xba\xf5\xbd\xef\xca\x93\xefZ@\xc1=\xf2H\x07c\xde )=\x88\x03\xef\x91\xb8\xee\x82\x96\x8f\x10Vo\xe7\xbd\xefe\x00\xee\xe5'
print("buff len",len(buff))

encoded = base64.b64encode (buff)

print(encoded)

i = 0
print("Length",len(encoded))
      
while (i < len(encoded)):
    print("i:",i, "char:",encoded[i])
    # print("c",encoded[i])
    i += 1

