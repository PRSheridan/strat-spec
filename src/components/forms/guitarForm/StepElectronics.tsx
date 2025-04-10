import { useEffect, useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const electronicsSchema = z
  .object({
    pickup_configuration: z.string(),
    pickups: z.array(z.string()).min(1, "Select at least one pickup"),
    show_other_controls: z.boolean().optional(),
    other_controls: z.string().nullable().optional(),
    hardware_finish: z.string().optional(),
    switch: z.string(),
    controls: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.show_other_controls && !data.other_controls?.trim()) {
      ctx.addIssue({
        path: ["other_controls"],
        code: z.ZodIssueCode.custom,
        message: "Please enter a description of the other controls",
      })
    }
  })

type ElectronicsData = z.infer<typeof electronicsSchema>

interface StepElectronicsProps {
  onNext: (data: ElectronicsData) => void
}

function StepElectronics({ onNext }: StepElectronicsProps) {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    setValue,
  } = useForm<ElectronicsData>({
    resolver: zodResolver(electronicsSchema),
    defaultValues: {
      pickup_configuration: "SSS",
      pickups: [],
      show_other_controls: false,
      other_controls: "",
      hardware_finish: "",
      switch: "",
      controls: "",
    },
  })

  const showOtherControls = watch("show_other_controls")

  const [pickupOptions, setPickupOptions] = useState<string[]>([])
  const [switchOptions, setSwitchOptions] = useState<string[]>([])
  const [controlOptions, setControlOptions] = useState<string[]>([])

  //not yet functional just examples
  useEffect(() => {
    fetch("/api/pickups")
      .then(res => res.json())
      .then(data => setPickupOptions(data.map((p: any) => p.type)))

    fetch("/api/switches")
      .then(res => res.json())
      .then(data => setSwitchOptions(data.map((s: any) => s.positions + "-way")))

    fetch("/api/controls")
      .then(res => res.json())
      .then(data => setControlOptions(data.map((c: any) => c.configuration)))
  }, [])

  function onSubmit(data: ElectronicsData) {
    console.log("Step 3 Data:", data)
    onNext(data)
  }

  return (
    <div className="guitar-block">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2>Step 3: Electronics</h2>

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

        <div className="guitar-block-section">
          <label>Pickups</label>
          <select multiple {...register("pickups")}>
            {pickupOptions.map((pickup) => (
              <option key={pickup} value={pickup}>{pickup}</option>
            ))}
          </select>
          {errors.pickups && <p>{errors.pickups.message}</p>}
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
            <option value="">Select a finish</option>
            <option value="Chrome">Chrome</option>
            <option value="Nickel">Nickel</option>
            <option value="Gold">Gold</option>
            <option value="Black">Black</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="guitar-block-section">
          <label>Switch</label>
          <select {...register("switch")}>
            <option value="">Select switch</option>
            {switchOptions.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
          {errors.switch && <p>{errors.switch.message}</p>}
        </div>

        <div className="guitar-block-section">
          <label>Controls</label>
          <select {...register("controls")}>
            <option value="">Select control layout</option>
            {controlOptions.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          {errors.controls && <p>{errors.controls.message}</p>}
        </div>

        <button type="submit">Next</button>
      </form>
    </div>
  )
}

export default StepElectronics