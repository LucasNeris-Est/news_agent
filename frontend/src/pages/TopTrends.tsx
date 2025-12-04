import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Link } from "wouter"
import { politicaTrends, legislacaoTrends, type Trend } from "@/data/mockData"

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
            <Link key={trend.id} href={`/trends/${encodeURIComponent(trend.keyword)}`}>
              <div className="flex items-center justify-between p-3 rounded-lg border hover:bg-accent transition-colors cursor-pointer">
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
            </Link>
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
