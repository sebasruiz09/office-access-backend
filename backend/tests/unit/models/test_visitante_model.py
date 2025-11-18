import pytest
from datetime import datetime
from models import Visitante, db

def test_visitante_creation():
    """Test de creación de un visitante con todos los campos"""
    visitante = Visitante(
        numero_identificacion='12345678',
        tipo_identificacion='DNI',
        nombres='Juan',
        apellidos='Pérez',
        tipo_visitante='Personal'
    )
    
    assert visitante.numero_identificacion == '12345678'
    assert visitante.tipo_identificacion == 'DNI'
    assert visitante.nombres == 'Juan'
    assert visitante.apellidos == 'Pérez'
    assert visitante.tipo_visitante == 'Personal'
    assert visitante.empresa_representa is None
    assert visitante.fecha_registro is None or isinstance(visitante.fecha_registro, datetime)

def test_visitante_empresarial():
    """Test de creación de un visitante empresarial"""
    visitante = Visitante(
        numero_identificacion='87654321',
        tipo_identificacion='RUC',
        nombres='Empresa',
        apellidos='S.A.',
        tipo_visitante='Empresarial',
        empresa_representa='Empresa S.A.'
    )
    
    assert visitante.tipo_visitante == 'Empresarial'
    assert visitante.empresa_representa == 'Empresa S.A.'

def test_visitante_to_dict():
    """Test del método to_dict"""
    visitante = Visitante(
        numero_identificacion='12345678',
        tipo_identificacion='DNI',
        nombres='Juan',
        apellidos='Pérez',
        tipo_visitante='Personal'
    )
    
    visitante_dict = visitante.to_dict()
    
    assert isinstance(visitante_dict, dict)
    assert visitante_dict['numero_identificacion'] == '12345678'
    assert visitante_dict['nombres'] == 'Juan'
    assert visitante_dict['apellidos'] == 'Pérez'
    assert 'fecha_registro' in visitante_dict

def test_visitante_repr():
    """Test del método __repr__"""
    visitante = Visitante(
        numero_identificacion='12345678',
        tipo_identificacion='DNI',
        nombres='Juan',
        apellidos='Pérez',
        tipo_visitante='Personal'
    )
    
    assert "Juan Pérez" in str(visitante)
