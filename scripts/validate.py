#!/usr/bin/env python3
"""
Validação de extrato de milhas LATAM Pass.
Uso: python validate.py personal/transactions.json --saldo 415531
"""

import json
import sys
import argparse

def validate(transactions_file, expected_saldo):
    with open(transactions_file) as f:
        tx = json.load(f)

    total = sum(t['m'] for t in tx)
    bonus = sum(t['m'] for t in tx if t['t'] == 'B')
    acumulo = sum(t['m'] for t in tx if t['t'] == 'A')

    # Monthly breakdown
    months = {}
    for t in tx:
        d = t['d']
        if d not in months:
            months[d] = {'total': 0, 'acumulo': 0, 'bonus': 0, 'itau_base': 0, 'itau_bonus': 0}
        months[d]['total'] += t['m']
        if t['t'] == 'B':
            months[d]['bonus'] += t['m']
        else:
            months[d]['acumulo'] += t['m']
        if t['s'] == 'Itaú LATAM Infinite':
            if t['t'] == 'A':
                months[d]['itau_base'] += t['m']
            else:
                months[d]['itau_bonus'] += t['m']

    print(f"{'='*60}")
    print(f"VALIDAÇÃO DE EXTRATO LATAM PASS")
    print(f"{'='*60}")
    print(f"Total:    {total:>10,}")
    print(f"Esperado: {expected_saldo:>10,}")
    print(f"Diff:     {total - expected_saldo:>10,}")
    print(f"Status:   {'✅ OK' if total == expected_saldo else '❌ DIFERENÇA ENCONTRADA'}")
    print(f"")
    print(f"Acúmulo:  {acumulo:>10,}")
    print(f"Bônus:    {bonus:>10,}")
    print(f"")

    # Check bonus cap
    print(f"{'MÊS':<10} {'TOTAL':>8} {'ACÚM':>8} {'BÔNUS':>8} {'ITAÚ%':>6}")
    print(f"{'-'*44}")
    for m in sorted(months.keys()):
        d = months[m]
        camp = round(d['itau_bonus'] / d['itau_base'] * 100) if d['itau_base'] > 0 else 0
        flag = ' ⚠️ CAP?' if d['bonus'] >= 29500 else ''
        print(f"{m:<10} {d['total']:>8,} {d['acumulo']:>8,} {d['bonus']:>8,} {camp:>5}%{flag}")

    # Check for potential issues
    print(f"\n{'='*60}")
    issues = []
    if total != expected_saldo:
        issues.append(f"❌ Total ({total:,}) ≠ Saldo ({expected_saldo:,}), diff: {total-expected_saldo:,}")

    for m in sorted(months.keys()):
        if months[m]['bonus'] > 30000:
            issues.append(f"⚠️  {m}: bônus {months[m]['bonus']:,} > cap 30.000")

    if issues:
        print("ISSUES:")
        for i in issues:
            print(f"  {i}")
    else:
        print("✅ Nenhum problema encontrado")

    return total == expected_saldo

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validar extrato de milhas LATAM Pass')
    parser.add_argument('file', help='Arquivo JSON de transações')
    parser.add_argument('--saldo', type=int, required=True, help='Saldo esperado')
    args = parser.parse_args()

    ok = validate(args.file, args.saldo)
    sys.exit(0 if ok else 1)
