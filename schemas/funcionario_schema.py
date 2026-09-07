from pydantic import BaseModel, EmailStr

class FuncionarioBaseSchema(BaseModel):
   nome: str
   endereco: str
   telefone: str
   salario: float

#O que o admin envia para cadastrar(Herda os dados acima + pede login)
class FuncionarioCreateSchema(FuncionarioBaseSchema):
   email: EmailStr
   senha: str

#O que a API devolve(Herda os dados publicos + adiconar o id e o e-mail).
class FuncionarioResponseSchema(FuncionarioBaseSchema):
   id: int
   email: EmailStr

   class Config:
      from_attributes = True

