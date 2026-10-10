# HikeFlora — entrega da Meta I

Esta é uma versão inicial completa para o grupo rever e editar. O relatório
tem **6 páginas**, dentro do limite de 10 páginas do enunciado. Os ficheiros
editáveis são `entrega/relatorio_meta1.docx`, `entrega/apresentacao_meta1.pptx`
e `entrega/anexo_prompts_ia.docx`; os PDFs correspondentes foram gerados a
partir deles.

## Ficheiro de submissão

`entrega/HikeFlora_MetaI.zip` reúne:

- `relatorio_meta1.pdf` — relatório para submeter;
- `apresentacao_meta1.pdf` e `apresentacao_meta1.pptx` — slides para defesa;
- `anexo_prompts_ia.pdf` e `anexo_prompts_ia.docx` — registo de IAG, com campos
  «Minha análise» assinalados como rascunhos a rever pelo grupo;
- `codigo/` — seis scripts Python, `selecao_imagens.csv` e `requirements.txt`;
- `resultados/` — históricos de treino e avaliação independente;
- `LEIA_PRIMEIRO.md` — instruções de reprodução.

O dataset extraído e `images.zip` não entram no Git. Os modelos `.keras` estão
no Git para partilha entre o grupo, mas não entram no ZIP de submissão. O manifesto
`selecao_imagens.csv` identifica exatamente as 11 000 fotografias usadas.
Fonte: https://zenodo.org/records/10419064.

## Antes da submissão definitiva

Rever os nomes e números dos autores, a redação do relatório, as referências,
as propostas do campo «Minha análise» do anexo e os slides. Depois de editar
um DOCX ou PPTX, exportar novamente o PDF correspondente e **recriar o ZIP**;
o ZIP atual não se atualiza sozinho.

No computador onde estão as imagens e os pesos dos modelos, o teste pode ser
reproduzido com `avaliar_teste.py`. A avaliação guardada em
`resultados/avaliacao_teste.txt` corresponde à execução já realizada pelo grupo.
