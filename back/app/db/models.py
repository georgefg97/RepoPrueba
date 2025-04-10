from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    reputacion = Column(Integer, default=100)
    plan = Column(Enum('free', 'premium'), default='free')
    verificado = Column(Boolean, default=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relación uno a muchos con Subastas
    subastas = relationship("Subasta", back_populates="subastador")

class Subasta(Base):
    __tablename__ = 'subastas'
    
    id = Column(Integer, primary_key=True, index=True)
    subastador_id = Column(Integer, ForeignKey('usuarios.id'))
    titulo = Column(String(200), nullable=False)
    descripcion = Column(String(500))
    tipo = Column(Enum('inglesa', 'holandesa'), default='inglesa')
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime)
    precio_inicial = Column(Float, nullable=False)
    precio_actual = Column(Float, nullable=False)
    estado = Column(Enum('activa', 'pausada', 'finalizada', 'cancelada'), default='activa')
    
    # Relación muchos a uno con Usuario
    subastador = relationship("Usuario", back_populates="subastas")
    
    # Relación uno a muchos con Pujas
    pujas = relationship("Puja", back_populates="subasta")
    
    # Relación uno a uno con Producto
    producto = relationship("Producto", uselist=False, back_populates="subasta")

class Puja(Base):
    __tablename__ = 'pujas'
    
    id = Column(Integer, primary_key=True, index=True)
    subasta_id = Column(Integer, ForeignKey('subastas.id'))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Relación muchos a uno con Subasta
    subasta = relationship("Subasta", back_populates="pujas")
    
    # Relación muchos a uno con Usuario
    usuario = relationship("Usuario")

class Producto(Base):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, index=True)
    subasta_id = Column(Integer, ForeignKey('subastas.id'))
    nombre = Column(String(200), nullable=False)
    imagen_url = Column(String(255))
    descripcion = Column(String(500))
    atributos = Column(JSON)
    
    # Relación uno a uno con Subasta
    subasta = relationship("Subasta", back_populates="producto")
    
    # Relación muchos a muchos con Tags
    tags = relationship("Tag", secondary="producto_tags", back_populates="productos")

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    # Relación muchos a muchos con Productos
    productos = relationship("Producto", secondary="producto_tags", back_populates="tags")

# Tabla de asociación para relación muchos a muchos Producto-Tag
class ProductoTags(Base):
    __tablename__ = 'producto_tags'
    
    producto_id = Column(Integer, ForeignKey('productos.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)