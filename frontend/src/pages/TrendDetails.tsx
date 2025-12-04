import { useRoute, Link } from "wouter"
import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, ExternalLink, Calendar, TrendingUp, Facebook, Instagram, Linkedin, Youtube, Twitter } from "lucide-react"

interface NewsArticle {
  id: number
  title: string
  source: string
  url: string
  publishedAt: string
  summary: string
  sentiment: "positive" | "neutral" | "negative"
}

interface SocialPost {
  id: number
  platform: string
  author: string
  content: string
  likes: number
  shares: number
  comments: number
  publishedAt: string
  url: string
}

type SocialPlatform = "X" | "Instagram" | "Facebook" | "LinkedIn" | "Reddit" | "YouTube"

// Dados mockados de notícias por keyword
const newsDatabase: Record<string, NewsArticle[]> = {
  "Eleições 2026": [
    {
      id: 1,
      title: "Partidos iniciam movimentação para eleições de 2026",
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

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const getSentimentColor = (sentiment: string): string => {
  switch (sentiment) {
    case "positive":
      return "bg-green-500 hover:bg-green-600"
    case "negative":
      return "bg-red-500 hover:bg-red-600"
    default:
      return "bg-blue-500 hover:bg-blue-600"
  }
}

const getSentimentLabel = (sentiment: string): string => {
  switch (sentiment) {
    case "positive":
      return "Positivo"
    case "negative":
      return "Negativo"
    default:
      return "Neutro"
  }
}

export default function TrendDetails() {
  const [, params] = useRoute("/trends/:keyword")
  const keyword = params?.keyword ? decodeURIComponent(params.keyword) : ""
  
  const articles = newsDatabase[keyword] || []
  const [selectedPlatform, setSelectedPlatform] = useState<SocialPlatform | null>(null)
  const [socialPosts, setSocialPosts] = useState<SocialPost[]>([])
  const [isExtracting, setIsExtracting] = useState(false)

  const platforms: { name: SocialPlatform; icon: any; color: string }[] = [
    { name: "X", icon: Twitter, color: "hover:bg-black hover:text-white" },
    { name: "Instagram", icon: Instagram, color: "hover:bg-gradient-to-tr hover:from-yellow-400 hover:via-pink-500 hover:to-purple-600 hover:text-white" },
    { name: "Facebook", icon: Facebook, color: "hover:bg-blue-600 hover:text-white" },
    { name: "LinkedIn", icon: Linkedin, color: "hover:bg-blue-700 hover:text-white" },
    { name: "Reddit", icon: () => <span className="text-xl font-bold">R</span>, color: "hover:bg-orange-600 hover:text-white" },
    { name: "YouTube", icon: Youtube, color: "hover:bg-red-600 hover:text-white" }
  ]

  const extractPosts = async () => {
    if (!selectedPlatform) return
    
    setIsExtracting(true)
    
    // Simula extração de posts (substituir por chamada real à API)
    setTimeout(() => {
      const mockPosts: SocialPost[] = Array.from({ length: 10 }, (_, i) => ({
        id: i + 1,
        platform: selectedPlatform,
        author: `@usuario${i + 1}`,
        content: `Post interessante sobre ${keyword} na plataforma ${selectedPlatform}. Este é um exemplo de conteúdo extraído da rede social. #${keyword.replace(/\s+/g, '')}`,
        likes: Math.floor(Math.random() * 10000),
        shares: Math.floor(Math.random() * 1000),
        comments: Math.floor(Math.random() * 500),
        publishedAt: new Date(Date.now() - Math.random() * 86400000).toISOString(),
        url: `https://${selectedPlatform.toLowerCase()}.com/post/${i + 1}`
      }))
      
      setSocialPosts(mockPosts)
      setIsExtracting(false)
    }, 2000)
  }

  return (
    <div className="container mx-auto p-6">
      <div className="mb-6">
        <Link href="/trends">
          <Button variant="ghost" size="sm" className="mb-4">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Voltar para Top Trends
          </Button>
        </Link>
        
        <div className="flex items-center gap-3 mb-2">
          <TrendingUp className="h-8 w-8 text-primary" />
          <h1 className="text-4xl font-bold tracking-tight">{keyword}</h1>
        </div>
        <p className="text-muted-foreground">
          Notícias relacionadas de diferentes fontes
        </p>
      </div>

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Total de Notícias</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{articles.length}</div>
            <p className="text-xs text-muted-foreground">De fontes verificadas</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Posts Extraídos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{socialPosts.length}</div>
            <p className="text-xs text-muted-foreground">De redes sociais</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Sentimento Geral</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">Neutro</div>
            <p className="text-xs text-muted-foreground">Baseado nas fontes</p>
          </CardContent>
        </Card>
      </div>

      {/* Seção de Extração de Posts de Redes Sociais */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Extrair Posts de Redes Sociais</CardTitle>
          <CardDescription>
            Selecione uma rede social para extrair posts relacionados a "{keyword}"
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
              {platforms.map((platform) => {
                const Icon = platform.icon
                return (
                  <Button
                    key={platform.name}
                    variant={selectedPlatform === platform.name ? "default" : "outline"}
                    className={`h-24 flex flex-col gap-2 ${selectedPlatform === platform.name ? '' : platform.color} transition-all`}
                    onClick={() => setSelectedPlatform(platform.name)}
                  >
                    <Icon className="h-8 w-8" />
                    <span className="text-xs font-medium">{platform.name}</span>
                  </Button>
                )
              })}
            </div>
            
            <Button
              onClick={extractPosts}
              disabled={!selectedPlatform || isExtracting}
              className="w-full"
              size="lg"
            >
              {isExtracting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Extraindo posts...
                </>
              ) : (
                `Extrair Posts do ${selectedPlatform || '...'}`
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Posts de Redes Sociais */}
      {socialPosts.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Posts do {selectedPlatform}</h2>
          <div className="space-y-4">
            {socialPosts.map((post) => (
              <Card key={post.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="outline">{post.platform}</Badge>
                        <span className="text-sm font-semibold">{post.author}</span>
                      </div>
                      <p className="text-sm">{post.content}</p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-6 text-sm text-muted-foreground mb-4">
                    <span>❤️ {post.likes.toLocaleString()} curtidas</span>
                    <span>🔄 {post.shares.toLocaleString()} compartilhamentos</span>
                    <span>💬 {post.comments.toLocaleString()} comentários</span>
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      {formatDate(post.publishedAt)}
                    </span>
                  </div>
                  <Button variant="outline" size="sm" asChild>
                    <a href={post.url} target="_blank" rel="noopener noreferrer">
                      Ver post original
                      <ExternalLink className="ml-2 h-4 w-4" />
                    </a>
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Notícias */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Notícias Relacionadas</h2>
        {articles.length === 0 ? (
          <Card>
            <CardContent className="flex items-center justify-center py-12">
              <p className="text-muted-foreground">Nenhuma notícia encontrada para este tópico.</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {articles.map((article) => (
              <Card key={article.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <CardTitle className="text-xl mb-2">{article.title}</CardTitle>
                      <CardDescription className="flex items-center gap-4 flex-wrap">
                        <span className="font-semibold text-foreground">{article.source}</span>
                        <span className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          {formatDate(article.publishedAt)}
                        </span>
                      </CardDescription>
                    </div>
                    <Badge className={getSentimentColor(article.sentiment)}>
                      {getSentimentLabel(article.sentiment)}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4">{article.summary}</p>
                  <Button variant="outline" size="sm" asChild>
                    <a href={article.url} target="_blank" rel="noopener noreferrer">
                      Ler notícia completa
                      <ExternalLink className="ml-2 h-4 w-4" />
                    </a>
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
