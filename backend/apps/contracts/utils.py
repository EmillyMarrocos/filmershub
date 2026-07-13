# ===========================================
# FILMERSHUB - UTILS DE CONTRATOS
# ===========================================

from django.utils import timezone


def generate_contract_html(contract):
    """Gera o HTML do contrato profissional."""
    clauses = contract.clauses.all().order_by('order')

    clauses_html = ''
    for i, clause in enumerate(clauses, 1):
        clauses_html += f'''
        <div class="clause">
            <h3>{i}. {clause.title}</h3>
            <p>{clause.content}</p>
        </div>'''

    if contract.additional_clauses:
        clauses_html += f'''
        <div class="clause">
            <h3>Cláusulas Adicionais</h3>
            <p>{contract.additional_clauses}</p>
        </div>'''

    client_signed_html = f'''
        <div class="signature-block">
            <div class="signature-line"></div>
            <p><strong>{contract.client.full_name}</strong></p>
            <p>Cliente</p>
            <p>Assinado em: {contract.client_signed_at.strftime('%d/%m/%Y %H:%M') if contract.client_signed_at else 'Pendente'}</p>
        </div>'''

    videomaker_signed_html = f'''
        <div class="signature-block">
            <div class="signature-line"></div>
            <p><strong>{contract.videomaker.full_name}</strong></p>
            <p>Videomaker</p>
            <p>Assinado em: {contract.videomaker_signed_at.strftime('%d/%m/%Y %H:%M') if contract.videomaker_signed_at else 'Pendente'}</p>
        </div>'''

    payment_methods = {
        'pix': 'PIX',
        'credit_card': 'Cartão de Crédito',
        'boleto': 'Boleto',
        'bank_transfer': 'Transferência Bancária',
    }

    service_types = dict(contract.SERVICE_TYPE_CHOICES)

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #1a1a2e;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #7C5CFC;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28pt;
            color: #7C5CFC;
            margin: 0 0 5px 0;
        }}
        .header h2 {{
            font-size: 16pt;
            color: #55556A;
            margin: 0;
            font-weight: normal;
        }}
        .contract-number {{
            text-align: center;
            font-size: 14pt;
            font-weight: bold;
            color: #7C5CFC;
            margin: 20px 0;
            padding: 10px;
            background: #f5f3ff;
            border-radius: 8px;
        }}
        .info-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .info-table td {{
            padding: 8px 12px;
            border-bottom: 1px solid #e8e8ed;
        }}
        .info-table td:first-child {{
            font-weight: bold;
            color: #55556A;
            width: 40%;
        }}
        .section-title {{
            font-size: 14pt;
            color: #7C5CFC;
            border-bottom: 2px solid #e8e8ed;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        .clause {{
            margin: 15px 0;
            padding: 10px;
            background: #fafafa;
            border-left: 3px solid #7C5CFC;
        }}
        .clause h3 {{
            font-size: 11pt;
            color: #1a1a2e;
            margin: 0 0 5px 0;
        }}
        .clause p {{
            margin: 0;
            color: #55556A;
        }}
        .signatures {{
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
            page-break-inside: avoid;
        }}
        .signature-block {{
            width: 45%;
            text-align: center;
        }}
        .signature-line {{
            border-bottom: 1px solid #1a1a2e;
            margin-bottom: 10px;
            height: 40px;
        }}
        .signature-block p {{
            margin: 3px 0;
            font-size: 10pt;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 15px;
            border-top: 2px solid #e8e8ed;
            text-align: center;
            font-size: 9pt;
            color: #8b8b9e;
        }}
        .hash {{
            font-family: monospace;
            font-size: 8pt;
            word-break: break-all;
            color: #8b8b9e;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>FilmersHub</h1>
        <h2>Contrato de Prestação de Serviços</h2>
    </div>

    <div class="contract-number">{contract.contract_number}</div>

    <h2 class="section-title">Dados do Contrato</h2>
    <table class="info-table">
        <tr>
            <td>Tipo de Serviço:</td>
            <td>{service_types.get(contract.service_type, contract.service_type)}</td>
        </tr>
        <tr>
            <td>Descrição:</td>
            <td>{contract.service_description}</td>
        </tr>
        <tr>
            <td>Data do Evento:</td>
            <td>{contract.event_date.strftime('%d/%m/%Y')}</td>
        </tr>
        <tr>
            <td>Data de Entrega:</td>
            <td>{contract.delivery_date.strftime('%d/%m/%Y')}</td>
        </tr>
        <tr>
            <td>Local:</td>
            <td>{contract.location}</td>
        </tr>
        <tr>
            <td>Valor Total:</td>
            <td>R$ {contract.total_value:,.2f}</td>
        </tr>
        <tr>
            <td>Forma de Pagamento:</td>
            <td>{payment_methods.get(contract.payment_method, contract.payment_method)}</td>
        </tr>
        <tr>
            <td>Status:</td>
            <td>{contract.get_status_display()}</td>
        </tr>
    </table>

    <h2 class="section-title">Partes</h2>
    <table class="info-table">
        <tr>
            <td>Videomaker:</td>
            <td>{contract.videomaker.full_name} ({contract.videomaker.email})</td>
        </tr>
        <tr>
            <td>Cliente:</td>
            <td>{contract.client.full_name} ({contract.client.email})</td>
        </tr>
    </table>

    <h2 class="section-title">Cláusulas</h2>
    {clauses_html}

    <div class="signatures">
        {client_signed_html}
        {videomaker_signed_html}
    </div>

    <div class="footer">
        <p>Contrato gerado por FilmersHub em {timezone.now().strftime('%d/%m/%Y às %H:%M')}</p>
        <p class="hash">Hash SHA-256: {contract.content_hash}</p>
    </div>
</body>
</html>'''

    return html


def generate_contract_pdf(contract):
    """Gera o PDF do contrato e retorna o objeto File."""
    from weasyprint import HTML
    from io import BytesIO
    from django.core.files.base import ContentFile

    html_content = generate_contract_html(contract)
    pdf_bytes = HTML(string=html_content).write_pdf()

    filename = f'{contract.contract_number}.pdf'
    content_file = ContentFile(pdf_bytes, name=filename)
    return content_file
