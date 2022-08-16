import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";
import { CategoryScale, ScriptableContext } from "chart.js";
import "chartjs-adapter-date-fns";
import { ptBR } from "date-fns/locale";
import api from "../../services/api";

Chart.register(CategoryScale);

type ChartsProps = {
  companyId: string;
};

export const Charts = ({ companyId }: ChartsProps) => {
  type CompanyDetail = {
    name: string;
    code: string;
    last_quote: number;
    data: { timestamp: Date; value: Number }[];
  };

  const [company, setCompany] = useState({} as CompanyDetail);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setIsLoading(true);

    api
      .get(`/companies/${companyId}/`)
      .then(({ data }) => {
        setCompany(data);
        setIsLoading(false);
      })
      .catch((error) => {
        setError(error);
        setIsLoading(false);
      });
  }, []);

  return (
    <>
      <Line
        data={{
          datasets: [
            {
              data: company.data,
              fill: "start",
              borderColor: "rgba(237, 91, 154, 1)",
              borderWidth: 2,
              backgroundColor: (context: ScriptableContext<"line">) => {
                const ctx = context.chart.ctx;
                const gradient = ctx.createLinearGradient(0, 0, 0, 200);
                gradient.addColorStop(0, "rgba(237, 91, 154, 1)");
                gradient.addColorStop(1, "rgba(237, 91, 154, 0.2)");
                return gradient;
              },
            },
          ],
        }}
        options={{
          responsive: true, // Responsividade
          plugins: {
            legend: {
              // Escondendo legenda superior
              display: false,
            },
          },
          elements: {
            line: {
              // Tornando linhas curvadas
              tension: 0.3,
            },
          },
          scales: {
            x: {
              // Definindo que o eixo x é baseado temporal
              type: "time",
              time: {
                unit: "hour",
              },
              adapters: {
                date: {
                  locale: ptBR,
                },
              },
            },
          },
          parsing: {
            // Definindo x e y
            xAxisKey: "timestamp",
            yAxisKey: "value",
          },
        }}
      />
    </>
  );
};
