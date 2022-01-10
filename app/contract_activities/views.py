from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .forms import ContractForm, CategoryForm
from .models import Contracts, Contractypes
from .. import db
from flask_login import login_user, current_user, logout_user, login_required
from . import contract_activities_blueprint
from datetime import datetime


@contract_activities_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def view_contract_info():
    form = ContractForm()
    contracts = Contracts.query.order_by(Contracts.deadline).all()
    return render_template('crud_contracts.html', contracts_list = contracts, form = form, user_id = current_user.id)


@contract_activities_blueprint.route('/add_contract', methods=['GET', 'POST'])
@login_required
def new_contract():
    form = ContractForm()
    form.contract_type.choices = [(type_c.type_id, type_c.type) for type_c in Contractypes.query.all()]
    if form.validate_on_submit():
        contract_data = Contracts(contract_code = form.contract_code.data, 
                            organization_name = form.organization_name.data,
                            deadline = form.deadline.data,
                            contract_amount = form.contract_amount.data,
                            contract_type = form.contract_type.data,
                            user_id = current_user.id)

        db.session.add(contract_data)
        db.session.commit()
        return redirect(url_for('contracts.view_contract_info'))
    contracts = Contracts.query.order_by(Contracts.contract_code).all()
    return render_template('new_contract_add.html', contracts_list = contracts, form = form)


@contract_activities_blueprint.route('/<id>', methods=['GET', 'POST'])
def detail_info_contract(id):
    print(id)
    contracts = Contracts.query.get_or_404(id)
    contract_type = Contractypes.query.get_or_404(contracts.contract_type)
    print(contract_type)
    return render_template('contract_full_info.html', contract = contracts, contract_type = contract_type)


@contract_activities_blueprint.route('/<id>/delete_contract', methods=['GET', 'POST'])
def delete_contract(id):
    contract = Contracts.query.get_or_404(id)
    if current_user.id == contract.user_id:
        db.session.delete(contract)
        db.session.commit()
        return redirect(url_for('contracts.view_contract_info'))
    flash('Це не ваш пост', category='warning')
    return redirect(url_for('contracts.detail_info_contract', id=contract.user_id))


@contract_activities_blueprint.route('/<id>/edit_contract', methods=['GET', 'POST'])
def edit_contract(id):
    contract = Contracts.query.get_or_404(id)
    if current_user.id != contract.user_id:
        flash('Це договір не є вашим!', category='warning')
        return redirect(url_for('contracts.detail_info_contract', contracts = contract, id = id))
    form = ContractForm()
    form.contract_type.choices = [(contract.type_id, contract.type) for contract in Contractypes.query.all()]
    if form.validate_on_submit():
        contract.organization_name = form.organization_name.data
        contract.contract_code = form.contract_code.data
        contract.deadline = form.deadline.data
        contract.contract_amount = form.contract_amount.data
        contract.contract_type = form.contract_type.data

        db.session.add(contract)
        db.session.commit()

        flash('Договір був оновлений', category='access')
        return redirect(url_for('contracts.detail_info_contract', id=id))
    contract.organization_name = form.organization_name.data
    contract.contract_code = form.contract_code.data
    contract.deadline = form.deadline.data
    contract.contract_amount = form.contract_amount.data
    contract.contract_type = form.contract_type.data

    return render_template('new_contract_add.html', form=form, contracts_list = contract)

@contract_activities_blueprint.route('/contract_types', methods=['GET', 'POST'])
@login_required
def contract_types_info():
    form = CategoryForm()
    types = Contractypes.query.order_by(Contractypes.type_id).all()
    return render_template('contract_types.html', contract_types = types, form = form, user_id = current_user.id)


@contract_activities_blueprint.route('/add_contract_type', methods=['GET', 'POST'])
@login_required
def contract_type_add():
    form = CategoryForm()

    if form.validate_on_submit():
        contract_type = Contractypes(type = form.contract_type.data)

        db.session.add(contract_type)
        db.session.commit()
        flash('Добавлений новий тип договору')
        return redirect(url_for('contracts.contract_types_info'))

    contract_types = Contractypes.query.all()
    return render_template('add_contract_type.html', contract_types=contract_types, form=form)


@contract_activities_blueprint.route('<id>/update_contract_type/', methods=['GET', 'POST'])
@login_required
def update_contract_type(id):
    contract_type = Contractypes.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        contract_type.type = form.contract_type.data

        db.session.add(contract_type)
        db.session.commit()
        flash('Тип договору оновлений')
        return redirect(url_for('contracts.contract_types_info'))

    form.contract_type.data = contract_type.type
    contract_types = Contractypes.query.all()
    return render_template('add_contract_type.html', contract_types = contract_types, form=form)


@contract_activities_blueprint.route('/<id>/delete_contract_type', methods=['GET'])
@login_required
def delete_contract_type(id):
    contract_type = Contractypes.query.get_or_404(id)
    db.session.delete(contract_type)
    db.session.commit()

    flash('Тип договору вилучено', category='access')
    return redirect(url_for('contracts.contract_types_info'))