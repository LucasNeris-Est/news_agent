export interface NewsArticle {
  id: number
  title: string
  source: string
  url: string
  publishedAt: string
  summary: string
  sentiment: "positive" | "neutral" | "negative"
}

export interface SocialPost {
  id: number
  platform: string
  author: string
  content: string
  likes: number
  shares: number
  comments: number
  publishedAt: string
  url: string
  disinfoScore?: number
  isAnalyzing?: boolean
}


export type SocialPlatform = "X" | "Instagram" | "Facebook" | "LinkedIn" | "Reddit" | "YouTube"

export interface Trend {
  id: number
  keyword: string
  searchVolume: number
  growth: number
}

export const politicaTrends: Trend[] = [
  { id: 1, keyword: "Eleições 2026", searchVolume: 125000, growth: 45 },
  { id: 2, keyword: "Reforma Tributária", searchVolume: 98000, growth: 32 },
  { id: 3, keyword: "Votação Congresso", searchVolume: 87000, growth: 28 },
  { id: 4, keyword: "Ministro STF", searchVolume: 76000, growth: 15 },
  { id: 5, keyword: "CPI Investigação", searchVolume: 65000, growth: 22 },
  { id: 6, keyword: "Partido Político", searchVolume: 54000, growth: -5 },
  { id: 7, keyword: "Declaração Presidente", searchVolume: 48000, growth: 18 },
  { id: 8, keyword: "Senado Federal", searchVolume: 42000, growth: 12 },
  { id: 9, keyword: "Câmara Deputados", searchVolume: 38000, growth: 8 },
  { id: 10, keyword: "Debate Político", searchVolume: 31000, growth: -3 }
]

export const legislacaoTrends: Trend[] = [
  { id: 1, keyword: "Nova Lei Trabalhista", searchVolume: 142000, growth: 52 },
  { id: 2, keyword: "Mudança CLT", searchVolume: 118000, growth: 38 },
  { id: 3, keyword: "Decreto Presidencial", searchVolume: 95000, growth: 41 },
  { id: 4, keyword: "Regulamentação Tributária", searchVolume: 89000, growth: 25 },
  { id: 5, keyword: "Lei Orçamentária", searchVolume: 72000, growth: 19 },
  { id: 6, keyword: "Medida Provisória", searchVolume: 68000, growth: 33 },
  { id: 7, keyword: "Projeto de Lei", searchVolume: 61000, growth: 15 },
  { id: 8, keyword: "Portaria Ministerial", searchVolume: 55000, growth: 28 },
  { id: 9, keyword: "Resolução Normativa", searchVolume: 47000, growth: 11 },
  { id: 10, keyword: "Emenda Constitucional", searchVolume: 39000, growth: 7 }
]

// Dados mockados de notícias por keyword
export const newsDatabase: Record<string, NewsArticle[]> = {
  "Eleições 2026": [
    {
      id: 1,
      title: "Partidos inchiciam movimentação para eleições de 2026",
      source: "G1",
      url: "https://g1.globo.com",
      publishedAt: "2025-12-03T10:30:00",
      summary: "Principais partidos políticos já começam a discutir estratégias e possíveis candidaturas para as eleições gerais de 2026.",
      sentiment: "neutral"
    },
    {
      id: 2,
      title: "TSE anuncia calendário preliminar das eleições 2026",
      source: "Folha de S.Paulo",
      url: "https://folha.uol.com.br",
      publishedAt: "2025-12-03T09:15:00",
      summary: "Tribunal Superior Eleitoral divulga cronograma inicial com datas importantes para o pleito de 2026.",
      sentiment: "positive"
    },
    {
      id: 3,
      title: "Pesquisa mostra cenário ainda indefinido para 2026",
      source: "O Globo",
      url: "https://oglobo.globo.com",
      publishedAt: "2025-12-02T14:20:00",
      summary: "Levantamento indica que eleitores ainda não têm candidato definido para as eleições presidenciais.",
      sentiment: "neutral"
    },
    {
      id: 4,
      title: "Governadores articulam candidaturas para próximo pleito",
      source: "Estadão",
      url: "https://estadao.com.br",
      publishedAt: "2025-12-02T11:45:00",
      summary: "Diversos governadores estaduais começam a se posicionar como potenciais candidatos à presidência em 2026.",
      sentiment: "neutral"
    },
    {
      id: 5,
      title: "Novas regras eleitorais podem impactar eleições 2026",
      source: "UOL",
      url: "https://uol.com.br",
      publishedAt: "2025-12-01T16:00:00",
      summary: "Mudanças na legislação eleitoral aprovadas recentemente devem alterar dinâmica das campanhas no próximo pleito.",
      sentiment: "negative"
    }
  ],
  "Reforma Tributária": [
    {
      id: 1,
      title: "Congresso aprova texto final da Reforma Tributária",
      source: "CNN Brasil",
      url: "https://cnnbrasil.com.br",
      publishedAt: "2025-12-03T13:00:00",
      summary: "Após meses de debate, parlamentares aprovam versão final da reforma que unifica impostos sobre consumo.",
      sentiment: "positive"
    },
    {
      id: 2,
      title: "Empresas se preparam para mudanças tributárias",
      source: "Valor Econômico",
      url: "https://valor.globo.com",
      publishedAt: "2025-12-03T08:30:00",
      summary: "Setor empresarial inicia adaptações aos novos modelos de tributação previstos na reforma.",
      sentiment: "neutral"
    },
    {
      id: 3,
      title: "Especialistas alertam sobre impactos da reforma",
      source: "InfoMoney",
      url: "https://infomoney.com.br",
      publishedAt: "2025-12-02T15:45:00",
      summary: "Economistas apontam possíveis efeitos da reforma tributária sobre diferentes setores da economia.",
      sentiment: "negative"
    },
    {
      id: 4,
      title: "Estados negociam transição da reforma tributária",
      source: "Metrópoles",
      url: "https://metropoles.com",
      publishedAt: "2025-12-02T10:20:00",
      summary: "Governadores discutem período de adaptação e compensações por perdas de arrecadação.",
      sentiment: "neutral"
    },
    {
      id: 5,
      title: "População ainda não compreende mudanças tributárias",
      source: "R7",
      url: "https://r7.com",
      publishedAt: "2025-12-01T12:15:00",
      summary: "Pesquisa mostra que maioria dos brasileiros não entende as alterações propostas pela reforma.",
      sentiment: "negative"
    }
  ]
}
