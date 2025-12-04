import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function MonitoramentoTrends() {
  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight">Monitoramento de Trends</h1>
        <p className="text-muted-foreground mt-2">
          Acompanhe as principais tendências e notícias em tempo real
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Trending Topics</CardTitle>
            <CardDescription>Tópicos mais populares agora</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Política</span>
                <span className="text-sm text-muted-foreground">1.2K posts</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Tecnologia</span>
                <span className="text-sm text-muted-foreground">850 posts</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Saúde</span>
                <span className="text-sm text-muted-foreground">620 posts</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Análises Recentes</CardTitle>
            <CardDescription>Últimas verificações realizadas</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-red-500"></div>
                  <span className="text-sm font-medium">Alto Risco</span>
                </div>
                <p className="text-sm text-muted-foreground line-clamp-2">
                  Notícia sobre vacinas contém informações falsas...
                </p>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-yellow-500"></div>
                  <span className="text-sm font-medium">Médio Risco</span>
                </div>
                <p className="text-sm text-muted-foreground line-clamp-2">
                  Post sobre economia requer verificação adicional...
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Estatísticas</CardTitle>
            <CardDescription>Resumo das últimas 24h</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Posts Analisados</span>
                <span className="text-2xl font-bold">2.4K</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Fake News Detectadas</span>
                <span className="text-2xl font-bold text-red-500">143</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Taxa de Precisão</span>
                <span className="text-2xl font-bold text-green-500">94%</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <Card>
          <CardHeader>
            <CardTitle>Feed de Monitoramento</CardTitle>
            <CardDescription>Acompanhe posts em tempo real</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="rounded-lg border p-4">
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <p className="text-sm font-medium">Facebook • há 2 minutos</p>
                    <p className="text-sm text-muted-foreground">
                      "Breaking: Cientistas descobrem cura milagrosa..."
                    </p>
                  </div>
                  <Button variant="outline" size="sm">
                    Analisar
                  </Button>
                </div>
              </div>

              <div className="rounded-lg border p-4">
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <p className="text-sm font-medium">Twitter • há 5 minutos</p>
                    <p className="text-sm text-muted-foreground">
                      "Governo anuncia nova medida polêmica..."
                    </p>
                  </div>
                  <Button variant="outline" size="sm">
                    Analisar
                  </Button>
                </div>
              </div>

              <div className="rounded-lg border p-4">
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <p className="text-sm font-medium">Instagram • há 8 minutos</p>
                    <p className="text-sm text-muted-foreground">
                      "Você não vai acreditar no que aconteceu..."
                    </p>
                  </div>
                  <Button variant="outline" size="sm">
                    Analisar
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
