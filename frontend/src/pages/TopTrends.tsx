import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface Trend {
  id: number
  keyword: string
  searchVolume: number
  growth: number
}

const politicaTrends: Trend[] = [
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

const legislacaoTrends: Trend[] = [
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

const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const TrendsList = ({ trends, category }: { trends: Trend[], category: string }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{category}</CardTitle>
        <CardDescription>Top 10 tendências mais buscadas</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {trends.map((trend, index) => (
            <div
              key={trend.id}
              className="flex items-center justify-between p-3 rounded-lg border hover:bg-accent transition-colors"
            >
              <div className="flex items-center gap-3 flex-1">
                <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 text-primary font-semibold text-sm">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <p className="font-medium text-sm">{trend.keyword}</p>
                  <p className="text-xs text-muted-foreground">
                    Volume: {formatNumber(trend.searchVolume)} buscas
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Badge
                  variant={trend.growth > 0 ? "default" : "secondary"}
                  className={
                    trend.growth > 0
                      ? "bg-green-500 hover:bg-green-600"
                      : trend.growth < 0
                      ? "bg-red-500 hover:bg-red-600"
                      : ""
                  }
                >
                  {trend.growth > 0 ? "+" : ""}{trend.growth}%
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

export default function TopTrends() {
  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight">Top Trends</h1>
        <p className="text-muted-foreground mt-2">
          Acompanhe as principais tendências de busca em Política e Legislação
        </p>
      </div>

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Total de Buscas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2.1M</div>
            <p className="text-xs text-muted-foreground">Nas últimas 24h</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Tendências Ativas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">20</div>
            <p className="text-xs text-muted-foreground">Em 2 categorias</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium">Crescimento Médio</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">+21.5%</div>
            <p className="text-xs text-muted-foreground">Comparado a ontem</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <TrendsList trends={politicaTrends} category="Política" />
        <TrendsList trends={legislacaoTrends} category="Legislação e Governo" />
      </div>
    </div>
  )
}
