import { useEffect, useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const physicalSpecsSchema = z
  .object({
    scale_length: z.number().min(24).max(27).nullable().optional(),
    weight: z.string().optional(),
    relic: z.enum(["None", "Light", "Medium", "Heavy", "Custom"]),
    plastic_color: z.string(),
    hardware_finish: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.weight && !/^(\d{1,2})\slbs\s(\d{1,2})\soz$/.test(data.weight)) {
      ctx.addIssue({
        path: ["weight"],
        code: z.ZodIssueCode.custom,
        message: 'Weight must be in the format "x lbs x oz"',
      })
    }
  })

type PhysicalSpecsData = z.infer<typeof physicalSpecsSchema>

interface StepPhysicalSpecsProps {
  onNext: (data: PhysicalSpecsData) => void
}

function StepPhysicalSpecs({ onNext }: StepPhysicalSpecsProps) {
  const [colorOptions, setColorOptions] = useState<string[]>([])
  const [finishOptions, setFinishOptions] = useState<string[]>([])

  useEffect(() => {
    fetch("/api/physical-form")
      .then(res => res.json())
      .then(data => {
        console.log(data)
        setColorOptions(data.plastic_colors)
        setFinishOptions(data.hardware_finishes)
      })
  }, [])

  const { register, handleSubmit, formState: { errors } } = useForm<PhysicalSpecsData>({
    resolver: zodResolver(physicalSpecsSchema),
    defaultValues: {
      scale_length: undefined,
      weight: undefined,
      relic: "None",
      plastic_color: "White",
      hardware_finish: "Chrome",
    },
  })

  const [pounds, setPounds] = useState(7)
  const [ounces, setOunces] = useState(0)

  function onSubmit(data: PhysicalSpecsData) {
    const combinedWeight = `${pounds} lbs ${ounces} oz`
    const finalData = { ...data, weight: combinedWeight }

    console.log("Step 2 Data:", finalData)
    onNext(finalData)
  }

  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2>Step 2: Physical Specs</h2>

        <div className="guitar-block-section">
          <label>Scale Length</label>
          <input
            type="number"
            step="any"
            {...register("scale_length", { valueAsNumber: true })}
            placeholder="Enter a scale length (24–27 inches)"
          />
        </div>

        <div className="guitar-block-section">
          <label>Weight</label>
          <div style={{ display: "flex", gap: "8px" }}>
            <select value={pounds} onChange={(e) => setPounds(Number(e.target.value))}>
              {[...Array(15)].map((_, i) => (
                <option key={i} value={i}>{i} lbs</option>
              ))}
            </select>

            <select value={ounces} onChange={(e) => setOunces(Number(e.target.value))}>
              {[...Array(16)].map((_, i) => (
                <option key={i} value={i}>{i} oz</option>
              ))}
            </select>
          </div>
          {errors.weight && <p>{errors.weight.message}</p>}
        </div>

        <div className="guitar-block-section">
          <label>Wear/Relic</label>
          <select {...register("relic")}>
            <option value="None">None</option>
            <option value="Light">Light</option>
            <option value="Medium">Medium</option>
            <option value="Heavy">Heavy</option>
            <option value="Custom">Custom</option>
          </select>
        </div>

        <div className="guitar-block-section">
          <label>Plastic Color</label>
          <select {...register("plastic_color")}>
            <option value="White">White</option>
            <option value="Black">Black</option>
            <option value="Cream">Cream</option>
            <option value="Mint Green">Mint Green</option>
            <option value="Parchment">Parchment</option>
            <option value="Aged White">Aged White</option>
            <option value="Pearloid">Pearloid</option>
            <option value="Tortoiseshell">Tortoiseshell</option>
            <option value="Anodized Gold">Anodized Gold</option>
            <option value="Gray">Gray</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="guitar-block-section">
          <label>Hardware Finish</label>
          <select {...register("hardware_finish")}>
            <option value="Chrome">Chrome</option>
            <option value="Nickel">Nickel</option>
            <option value="Gold">Gold</option>
            <option value="Black">Black</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <button type="submit">Next</button>
      </form>
    </div>
  )
}


export default StepPhysicalSpecs