WITH financeiro_recente AS (
    SELECT
        fi.candidato_id,
        fi.data_pagamento,
        fi.criacao,
        -- A partição aqui define o que é uma "tentativa de matrícula" única
        ROW_NUMBER() OVER(PARTITION BY fi.candidato_id, fi.tipo_cobranca_id ORDER BY fi.criacao DESC) as rn
    FROM
        fin.financeiro fi
    WHERE
        fi.tipo_cobranca_id = 1 -- Tipo Cobrança de Matrícula
)
SELECT
    p.nome,
    to_char(c.criacao, 'DD/MM/YYYY HH24:MI') as data_hora_inscricao,
    coalesce(c3.nome, 'N/A') as curso,
    coalesce(f.nome, 'N/A') as filial,
    CASE
        WHEN fr.data_pagamento IS NULL THEN 'Pagamento Pendente'
        ELSE 'Matriculado'
    END as status,
    coalesce(cont.valor, 'Sem e-mail') as email,
    coalesce(c4.nome, 'Sem concurso') as concurso
FROM
    public.aluno a
JOIN aca.candidato c ON c.id = a.candidato_id
JOIN public.pessoa p ON c.pessoa_id = p.id
JOIN aca.curriculo c2 ON c2.id = a.curriculo_id
JOIN public.curso c3 ON c3.id = c2.curso_id
JOIN public.filial f ON a.filial_id = f.id
JOIN aca.concurso_filial cf ON cf.id = c.concurso_filial_id
JOIN aca.concurso c4 ON c4.id = cf.concurso_id
JOIN contato cont ON cont.pessoa_id = p.id AND cont.tipo_contato_id = 1
LEFT JOIN financeiro_recente fr ON fr.candidato_id = c.id AND fr.rn = 1
WHERE
    c.exclusao IS NULL
    AND a.exclusao IS NULL
    AND (CAST($P{data.inicio} AS DATE) IS NULL OR c.criacao >= $P{data.inicio})
    AND (CAST($P{data.final} AS DATE) IS NULL OR c.criacao <= $P{data.final})
    AND (CAST($P{concurso_id} AS INTEGER) IS NULL OR c4.id = $P{concurso_id})
    AND (CAST($P{processo_seletivo_id} AS INTEGER) IS NULL OR c4.processo_seletivo_id = $P{processo_seletivo_id})
ORDER BY
    c.criacao,
    p.nome;
