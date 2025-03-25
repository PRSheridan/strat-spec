import { useState, useEffect }  from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const block3Schema = z
  .object({
    scale_length: z.number().min(20).max(30).nullable().optional(),
    weight: z.string().nullable().optional().refine(
      (val) =>
        val === null ||
        val === undefined ||
        /^(\d{1,2})\slbs\s(\d{1,2})\soz$/.test(val),
      { message: 'Weight must be in the format "x lbs x oz"' }),
    relic: z.enum(['None', 'Light', 'Medium', 'Heavy', 'Custom']),
    other_controls: z.string().nullable().optional(),
    hardware_finish: z.string().nullable().optional(),
    pickup_configuration: z.string()
  })

type Block3Data = z.infer<typeof block3Schema>

interface GuitarBlock3Props {
  onNext: (data: Block3Data) => void
}

function GuitarBlock3({ onNext }: GuitarBlock3Props) {
  const { register, handleSubmit, formState: { errors } } = useForm<Block3Data>({
    resolver: zodResolver(block3Schema),
    defaultValues: {
      scale_length: undefined,
      weight: undefined,
      relic: "None",
      other_controls: undefined, 
      hardware_finish: undefined,
      pickup_configuration: "SSS"
    },
  })

  function onSubmit(data:Block3Data) {
    console.log("Block 3 Data:", data)
    onNext(data)
  }
  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2>Block 2: Personalization</h2>

        <div>
          <label>Scale length</label>
          <input type="number" {...register("scale_length", { valueAsNumber: true })}
                 placeholder="Enter a scale length (20-30 inches)"/>
        </div>

        <div>
          <label>Weight</label>
          <input {...register("weight")} placeholder="Enter weight (e.g. 7 lbs 8 oz)" />
        </div>

        <div>
          <label>Relic</label>
          <select {...register("relic")}>
            <option value="None">None</option>
            <option value="Light">Light</option>
            <option value="Medium">Medium</option>
            <option value="Heavy">Heavy</option>
            <option value="Custom">Custom</option>
          </select>
        </div>

        <div>
          <label>Other controls</label>
          <textarea {...register("other_controls")} placeholder="Enter other controls" />
        </div>

        <div>
          <label>Hardware finish</label>
          <input {...register("hardware_finish")} placeholder="Enter hardware finish" />
        </div>

        <div>
          <label>Pickup configuration</label>
          <select {...register("pickup_configuration")}>
            <option value="SSS">SSS</option>
            <option value="Light">HSS</option>
            <option value="Medium">HSH</option>
            <option value="Heavy">HH</option>
            <option value="Custom">SS</option>
            <option value="Custom">Other</option>
          </select>
        </div>

        <button type="submit">Next</button>

      </form>
    </div>
  )
}

export default GuitarBlock3