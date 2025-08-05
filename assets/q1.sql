select
 f.numero_parcela as parcela,
 tc.nome as tipo_cobranca,
 TO_CHAR(f.competencia, 'MM/YYYY') as competencia,
 TO_CHAR(f.data_vencimento, 'DD/MM/YYYY') as vencimento,
 'R$ ' || replace(TO_CHAR(ROUND(coalesce(f.valor_ate_vencimento, 0), 2),
                             'FM999G999G990D00'), '.', ',') as valor_ate_vencimento,
 coalesce(TO_CHAR(f.data_pagamento, 'DD/MM/YYYY'), 'Não pago') as data_pagamento,
 'R$ ' || replace(TO_CHAR(ROUND(coalesce(f.valor_pago, 0), 2),
                             'FM999G999G990D00'), '.', ',') as valor_pago,
 s.nome as status,
 p.nome as aluno,
 a.ra as ra,
 c.nome as curso,
 f2.nome as filial
from
 fin.financeiro f
join fin.tipo_cobranca tc on
 tc.id = f.tipo_cobranca_id
join public.status s on
 s.id = f.status_id
join public.aluno a on
 a.id = f.aluno_id
join public.pessoa p on
 p.id = a.pessoa_id
join aca.matricula m on
 m.aluno_id = a.id
join public.curso c on
 c.id = m.curso_id
join public.filial f2 on
 f2.id = a.filial_id
where
 f.exclusao is null
 and a.exclusao is null
 and (cast($P{data.inicio} as DATE) is null
  or f.data_vencimento >= $P{data.inicio})
 and (cast($P{data.final} as DATE) is null
  or f.data_vencimento <= $P{data.final})
 and (cast($P{nome_aluno} as TEXT) is null
  or p.nome = $P{nome_aluno})
 and (cast($P{ra} as TEXT) is null
  or a.ra = $P{ra})
 and (cast($P{tipo_cobranca} as INTEGER) is null
  or tc.id = $P{tipo_cobranca})
 and (cast($P{curso_id} as INTEGER) is null
  or c.id = $P{curso_id})
 and (cast($P{polo_id} as INTEGER) is null
  or f2.id = $P{polo_id})
group by
 f.numero_parcela,
 tc.nome,
 f.competencia,
 f.data_vencimento,
 f.valor_ate_vencimento,
 f.data_pagamento,
 f.valor_pago,
 s.nome,
 p.nome,
 a.ra,
 c.nome,
 f2.nome
order by
 f.data_vencimento,
 aluno,
 curso,
 tipo_cobranca,
 parcela,
 vencimento;
