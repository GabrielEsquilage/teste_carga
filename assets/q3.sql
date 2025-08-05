with alunos_curso as (
select
 c.nome as curso,
 ne.nome as tipo_curso,
 f.nome as filial,
 row_number() over (
            partition by c.id,
 a.pessoa_id,
 f.id
order by
 m.criacao desc
        ) as rn
from
 public.aluno a
join aca.matricula m on
 m.aluno_id = a.id
join public.curso c on
 c.id = m.curso_id
join aca.nivel_ensino ne on
 ne.id = c.nivel_ensino_id
join public.filial f on
 f.id = a.filial_id
where
 a.exclusao is null
 and a.ativo = true
 and a.status_id = 17
 and m.ativo = true
 and m.exclusao is null
 and m.status_id = 20
 and (cast($P{dataInicio} as DATE) is null
  or a.criacao >= $P{dataInicio})
 and (cast($P{dataFinal} as DATE) is null
  or a.criacao <= $P{dataFinal})
 and ($P{filialId} is null
  or f.id = any(string_to_array($P{filialId}, ',')::int[]))
 and (
            $P{processoSeletivoId} is null
  and $P{concursoId} is null
  or exists (
  select
   1
  from
   aca.oferta o
  join aca.concurso c2 on
   c2.id = o.concurso_id
  join aca.processo_seletivo ps on
   ps.id = c2.processo_seletivo_id
  where
   o.filial_id = f.id
   and ($P{processoSeletivoId} is null
    or ps.id = any(string_to_array($P{processoSeletivoId}, ',')::int[]))
    and ($P{concursoId} is null
     or c2.id = any(string_to_array($P{concursoId}, ',')::int[]))
        )
      )
),
alunos_filtrados as (
select
 *
from
 alunos_curso
where
 rn = 1
),
agrupados as (
select
 filial,
 curso,
 tipo_curso,
 COUNT(*) as qtd_alunos
from
 alunos_filtrados
group by
 filial,
 curso,
 tipo_curso
)
select
 filial,
 curso,
 tipo_curso,
 qtd_alunos,
 SUM(qtd_alunos) over (partition by filial) as qtde_alunos_por_filial,
 SUM(qtd_alunos) over () as qtd_total_alunos
from
 agrupados
order by
 filial,
 curso;
