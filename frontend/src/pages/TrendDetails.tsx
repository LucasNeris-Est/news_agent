import { useRoute, Link } from "wouter"
import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, ExternalLink, Calendar, TrendingUp, Facebook, Instagram, Linkedin, Youtube, Twitter } from "lucide-react"
import { newsDatabase, type NewsArticle, type SocialPost, type SocialPlatform } from "@/data/mockData"

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
        url: `https://${selectedPlatform.toLowerCase()}.com/post/${i + 1}`,
        disinfoScore: undefined,
        isAnalyzing: false
      }))
      
      setSocialPosts(mockPosts)
      setIsExtracting(false)
    }, 2000)
  }

  const analyzeDisinformation = (postId: number) => {
    // Marca o post como analisando
    setSocialPosts(posts => 
      posts.map(post => 
        post.id === postId ? { ...post, isAnalyzing: true } : post
      )
    )

    // Simula análise de desinformação (substituir por chamada real à API)
    setTimeout(() => {
      const score = Math.floor(Math.random() * 100)
      
      setSocialPosts(posts => 
        posts.map(post => 
          post.id === postId 
            ? { ...post, disinfoScore: score, isAnalyzing: false }
            : post
        )
      )
    }, 3000)
  }

  const getDisinfoColor = (score: number): string => {
    if (score >= 70) return "text-red-600"
    if (score >= 40) return "text-yellow-600"
    return "text-green-600"
  }

  const getDisinfoLabel = (score: number): string => {
    if (score >= 70) return "Alto Risco"
    if (score >= 40) return "Risco Moderado"
    return "Baixo Risco"
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
                  
                  {post.disinfoScore !== undefined && (
                    <div className="mb-4 p-3 rounded-lg bg-muted">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium">Potencial de Desinformação:</span>
                        <div className="flex items-center gap-2">
                          <span className={`text-2xl font-bold ${getDisinfoColor(post.disinfoScore)}`}>
                            {post.disinfoScore}%
                          </span>
                          <Badge variant={post.disinfoScore >= 70 ? "destructive" : post.disinfoScore >= 40 ? "default" : "secondary"}>
                            {getDisinfoLabel(post.disinfoScore)}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" asChild>
                      <a href={post.url} target="_blank" rel="noopener noreferrer">
                        Ver post original
                        <ExternalLink className="ml-2 h-4 w-4" />
                      </a>
                    </Button>
                    <Button 
                      variant="default" 
                      size="sm"
                      onClick={() => analyzeDisinformation(post.id)}
                      disabled={post.isAnalyzing || post.disinfoScore !== undefined}
                    >
                      {post.isAnalyzing ? (
                        <>
                          <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-2"></div>
                          Analisando...
                        </>
                      ) : post.disinfoScore !== undefined ? (
                        "Já analisado"
                      ) : (
                        "Verificar potencial de desinformação"
                      )}
                    </Button>
                  </div>
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
