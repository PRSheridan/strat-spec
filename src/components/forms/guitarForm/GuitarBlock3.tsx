import { useState } from 'react'
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const block3Schema = z
  .object({
    scale_length: z.number().min(24).max(27).nullable().optional(),
    weight: z.string().optional(),
    relic: z.enum(['None', 'Light', 'Medium', 'Heavy', 'Custom']),
    show_other_controls: z.boolean().optional(),
    other_controls: z.string().nullable().optional(),
    hardware_finish: z.string().nullable().optional(),
    pickup_configuration: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.show_other_controls && !data.other_controls?.trim()) {
      ctx.addIssue({
        path: ["other_controls"],
        code: z.ZodIssueCode.custom,
        message: "Please enter a description of the other controls",
      })
    }

    if (data.weight && !/^(\d{1,2})\slbs\s(\d{1,2})\soz$/.test(data.weight)) {
      ctx.addIssue({
        path: ["weight"],
        code: z.ZodIssueCode.custom,
        message: 'Weight must be in the format "x lbs x oz"',
      })
    }
  })



type Block3Data = z.infer<typeof block3Schema>

interface GuitarBlock3Props {
  onNext: (data: Block3Data) => void
}

function GuitarBlock3({ onNext }: GuitarBlock3Props) {
  const { register, handleSubmit, watch, formState: { errors } } = useForm<Block3Data>({
    resolver: zodResolver(block3Schema),
    defaultValues: {
      scale_length: undefined,
      weight: undefined,
      relic: "None",
      show_other_controls: false,
      other_controls: "",
      hardware_finish: undefined,
      pickup_configuration: "SSS"
    },
  })

  const [pounds, setPounds] = useState(7)
  const [ounces, setOunces] = useState(0)
  
  const showOtherControls = watch("show_other_controls")

  function onSubmit(data: Block3Data) {
    const combinedWeight = `${pounds} lbs ${ounces} oz`
    const finalData = { ...data, weight: combinedWeight }
  
    console.log("Block 3 Data:", finalData)
    onNext(finalData)
  }

  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2>Block 3: Specs & Configuration</h2>

        <div className="guitar-block-section">
          <label>Scale Length</label>
          <input
            type="number"
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

        <div className="guitar-block-section inline">
          <label>Other Controls?</label>
          <label className="guitar-switch">
            <input type="checkbox" {...register("show_other_controls")} />
            <span className="guitar-slider" />
          </label>
        </div>

        {showOtherControls && (
          <div className="guitar-block-section">
            <label>Describe Other Controls</label>
            <textarea
              {...register("other_controls")}
              placeholder="Enter other controls"
            />
            {errors.other_controls && <p>{errors.other_controls.message}</p>}
          </div>
        )}

        <div className="guitar-block-section">
          <label>Hardware Finish</label>
          <select {...register("hardware_finish")}>
            <option value="Chrome">HH</option>
            <option value="Nickel">SS</option>
            <option value="Gold">Other</option>
            <option value="Black">Other</option>
            <option value="Other">HH</option>
          </select>
        </div>

        <div className="guitar-block-section">
          <label>Pickup Configuration</label>
          <select {...register("pickup_configuration")}>
            <option value="SSS">SSS</option>
            <option value="HSS">HSS</option>
            <option value="HSH">HSH</option>
            <option value="HH">HH</option>
            <option value="SS">SS</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <button type="submit">Next</button>
      </form>
    </div>
  )
}

export default GuitarBlock3
