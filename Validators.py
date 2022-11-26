class IMMETA(type):
    def __new__(cls,name,base,attrs,**kwargs):
        super_new = super().__new__
        print('new',attrs)
        ex = attrs.get('ex')
        setattr(ex,'aa','not written in dream')
        return super_new(cls,name,base,attrs,)
       
class ExtraClass():
    extra='imextra'
    def __init__(self,*args,**kwargs) -> None:
        print("extra init",kwargs)

    def get_aa(self):
        print(self.aa)

class QueueConstraintValidator(metaclass=IMMETA):

    def __init__(self,*args,**kwargs) -> None:
        print('quevalid init',kwargs)

    ex = ExtraClass()


qc = QueueConstraintValidator()
print(qc)
qc.ex.get_aa()
