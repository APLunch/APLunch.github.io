---
title: "Reinforcement Learning based Mixed Palletization"
excerpt: "A robust, investor-ready demo of mixed palletization using PPO reinforcement learning in Unity for high space utilization. <br/><img src='/images/Good Material/MixedPalletization.GIF' width=500>"
collection: portfolio
---

<img src='/images/Good Material/MixedPalletizationTraining2.gif' width=800>

<img src='/images/Good Material/Mixed Palletization Training.gif' width=800>

## Objective
Build a robust, investor-ready demo of mixed palletization in Unity that learns to place 3–5 SKUs onto a pallet for high space utilization while respecting basic safety and stability rules. The agent should plan with a short look-ahead queue of incoming boxes, choose rotation (0°/90°), and place boxes to form flat, layer-like stacks rather than risky tall columns.

## Technical Summary
We discretize the pallet (cell size = GCD of SKU lengths/widths) and maintain a height-map. Observations = height-map + the next k boxes' normalized (l, w, h) (no one-hot needed). The discrete action flattens (box-choice, rotation, i, j), with action-masking to block invalid moves (support ≥ threshold, no collision, stay under max height / "no deep stack"). 

PPO trains across many parallel arenas; for larger grids we use a lightweight "match-3-style" CNN encoder feeding small MLP heads; episodes end when no valid placements remain; reward = normalized volume gain. The trained policies export to ONNX for Unity runtime inference, enabling demo-ready deployment with photoreal assets and placement animation.

## Results
The agent reliably achieves ~0.68–0.73 pallet volume utilization in simulation after ~10M steps, with 5-SKU runs reaching ~0.73 under our heuristic constraints and stricter post-placement height caps yielding ~0.69. 

Policies train in parallel (dozens of arenas) and avoid high towers, preferring layer fill. The setup successfully demonstrates real-time inference with visually compelling photoreal assets, making it investor-ready for demonstrations.

## Detailed Documentation
Restricted by non-disclosure agreements.
