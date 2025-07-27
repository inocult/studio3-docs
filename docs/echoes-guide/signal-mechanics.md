# Signal Mechanics

## The Technical Details of Belief and Doubt

<div class="arena-card" markdown="1">

<h3>⚙️ How Signals Actually Work</h3>

Understanding the mechanics behind signaling is crucial for maximizing returns and minimizing risks. This guide covers the technical details, mathematical models, and strategic considerations of the signal system.

</div>

## Signal Types Deep Dive

### Belief Signals

<div class="arena-card" markdown="1">

<h3>✅ Positive Conviction Mechanics</h3>

**Technical Specifications:** Minimum Stake:** 10 $SIGNAL**
- **Maximum Stake:** Lock Period:
- **Success Multiplier:** Failure Result:
- ** Multiplier Formula:**
```
Base Multiplier × Time Bonus × Reputation Modifier × Phase Factor
```

</div>

### Doubt Signals

<div class="arena-card" markdown="1">

<h3>❌ Negative Conviction Mechanics</h3>

**Technical Specifications:** Minimum Stake:** 10 $SIGNAL**
- **Maximum Stake:** Lock Period:
- **Success Multiplier:** Failure Result:
- ** Multiplier Formula:**
```
Base Multiplier × Contrarian Bonus × Accuracy Streak × Risk Factor
```

</div>

## Multiplier System

### Base Multipliers

| Signal Type | Outcome | Base Range |
|------------|---------|------------|
| Belief | Success | 1.5x - 2.0x |
| Belief | Failure | 0x (burn) |
| Doubt | Success | 1.2x - 1.5x |
| Doubt | Failure | 0x (burn) |

### Bonus Modifiers

<div class="arena-card" markdown="1">

<h3>🎯 Multiplier Bonuses</h3>

**Time Bonus (Early Signals):**
- First 10% of pool: +0.5x
- First 25% of pool: +0.3x
- First 50% of pool: +0.1x
- After 50%: No bonus

**Reputation Modifier:**
- 0-100 XP: 1.0x
- 100-500 XP: 1.1x
- 500-2000 XP: 1.2x
- 2000+ XP: 1.3x

**Phase Factor:**
- Spark/Forge: 1.5x
- Ignition: 1.3x
- Drift: 1.2x
- Orbit/Flare: 1.1x
- Ascension: 1.0x

</div>

## Staking Mechanics

### The Staking Process

<div class="arena-card" markdown="1">

<h3>🔐 Technical Flow</h3>

1. **Signal Initiation**
   ```javascript
   function createSignal(ventureId, signalType, amount) {
     validateStake(amount);
     checkVentureStatus(ventureId);
     lockTokens(msg.sender, amount);
     recordSignal(signalDetails);
   }
   ```

2. **Token Locking**
   - Tokens transferred to escrow
   - Cannot be withdrawn
   - Tracked on-chain
   - Visible in UI

3. **Settlement Trigger**
   - Anchor validates milestone
   - Smart contract executes
   - Rewards calculated
   - Tokens distributed

</div>

### Gas Optimization

**Cost Considerations:**
- Signal creation: ~50,000 gas
- Batch signals: ~30,000 gas each
- Claim rewards: ~80,000 gas
- Emergency exit: ~100,000 gas

**Optimization Tips:**
- Batch multiple signals
- Time for low gas periods
- Use meta-transactions
- Claim rewards together

## Pool Dynamics

### Signal Pool Mechanics

<div class="arena-card" markdown="1">

<h3>🏊 Pool Behavior</h3>

**Pool Formation:**
- Starts empty at milestone declaration
- Grows with each signal
- Belief and doubt tracked separately
- Ratio affects multipliers

**Pool Metrics:**
```
Total Pool = Belief Stakes + Doubt Stakes
Belief Ratio = Belief Stakes / Total Pool
Sentiment = (Belief - Doubt) / Total Pool
```

**Dynamic Adjustments:**
- High belief ratio → Lower belief multipliers
- High doubt ratio → Lower doubt multipliers
- Balanced pools → Optimal returns
- Extreme ratios → Contrarian opportunities

</div>

### Liquidity Considerations

**Pool Depth Effects:**
- Shallow pools: Higher volatility
- Deep pools: More stability
- Early signals: Price discovery
- Late signals: Efficient market

## Advanced Signal Types

### Conditional Signals

<div class="arena-card" markdown="1">

<h3>🔄 Complex Signaling</h3>

**Types Available:**
1. **Time-Conditional**
   - "I believe IF completed by date X"
   - Different multipliers for time ranges
   - Partial rewards possible

2. **Outcome-Conditional**
   - "I believe IF metric Y achieved"
   - Specific success criteria
   - Binary or graduated rewards

3. **Sequential Signals**
   - Multi-milestone commitments
   - Compounding rewards
   - Higher risk/reward

</div>

### Hedged Positions

**Hedging Strategies:**
- Belief + smaller doubt position
- Across similar ventures
- Time-staggered entries
- Phase diversification

## Signal Timing

### Optimal Entry Points

<div class="arena-card" markdown="1">

<h3>⏰ Timing Your Signals</h3>

**Early Stage (0-20% filled):** Pros:** Maximum multipliers, first-mover advantage**
- **Cons:** Best for:
- ** Growth Stage (20-60% filled):** Some validation, decent multipliers
- **Cons:** Best for:
- ** Late Stage (60-90% filled):** Maximum information, lower risk
- **Cons:** Best for:
- ** Final Stage (90-100% filled):** Near-certain outcomes
- **Cons:** Best for:
</div>

## Risk Calculations

### Mathematical Models

<div class="arena-card" markdown="1">

<h3>📊 Risk/Reward Analysis</h3>

**Expected Value Formula:**
```
EV = (Success Probability × Reward Multiplier × Stake) - 
     (Failure Probability × Stake)
```

**Example Calculation:**
- Stake: 1,000 $SIGNAL
- Success chance: 70%
- Multiplier: 2.0x
- EV = (0.7 × 2.0 × 1,000) - (0.3 × 1,000)
- EV = 1,400 - 300 = 1,100 $SIGNAL

**Break-even Success Rate:**
```
Break-even = 1 / Multiplier
2.0x multiplier = 50% success needed
1.5x multiplier = 67% success needed
3.0x multiplier = 33% success needed
```

</div>

### Portfolio Risk Management

**Optimal Allocation:**
- No single signal > 10% of bankroll
- Phase diversification
- Venture diversification
- Belief/doubt balance

## Settlement Process

### How Rewards Distribute

<div class="arena-card" markdown="1">

<h3>💰 Settlement Mechanics</h3>

**Success Settlement:**
1. Anchor validates success
2. Smart contract triggered
3. Doubt stakes burned
4. Belief rewards calculated
5. Tokens distributed
6. XP awarded

**Failure Settlement:**
1. Anchor validates failure
2. Smart contract triggered
3. Belief stakes burned
4. Doubt rewards calculated
5. Tokens distributed
6. XP adjusted

</div>

### Emergency Procedures

**Force Exit Conditions:**
- Venture abandonment
- Smart contract issues
- Governance intervention
- Extended delays

**Emergency Exit Cost:**
- 90% token return
- 10% penalty burn
- No XP gained/lost
- Reputation impact

## Gas and Fees

### Transaction Costs

<div class="arena-card" markdown="1">

<h3>⛽ Fee Structure</h3>

**Platform Fees:**
- Signal creation: 0.5% of stake
- Reward claim: 1% of profit
- Emergency exit: 10% penalty
- No maintenance fees

**Network Fees:**
- Vary by congestion
- ~$5-50 per transaction
- Batch for savings
- Time for low periods

</div>

## Technical Integration

### API Access

**Available Endpoints:**
```javascript
GET /api/signals/{userId} - Your signals
GET /api/ventures/{ventureId}/signals - Venture signals
POST /api/signals/create - Create signal
GET /api/signals/{signalId}/status - Check status
```

### Smart Contract Interface

**Key Functions:**
```solidity
createSignal(uint ventureId, bool belief, uint amount)
claimRewards(uint signalId)
emergencyExit(uint signalId)
getSignalDetails(uint signalId)
```

## Monitoring Tools

### Signal Tracking

<div class="arena-card" markdown="1">

<h3>📈 Performance Monitoring</h3>

**Dashboard Metrics:**
- Active signals status
- Pending settlements
- Historical performance
- ROI calculations
- Risk exposure

**Alert System:**
- Milestone deadlines
- Settlement notifications
- Pool movements
- Opportunity alerts

</div>

## Advanced Strategies

### Arbitrage Opportunities

**Types of Arbitrage:**
- Cross-venture similar milestones
- Time-based mispricings
- Information asymmetry
- Sentiment extremes

### Algorithmic Signaling

**Automated Strategies:**
- Rule-based entries
- Portfolio rebalancing
- Risk management
- Sentiment following

## Common Technical Issues

### Troubleshooting

<div class="arena-card" markdown="1">

<h3>🔧 Problem Resolution</h3>

**Transaction Failures:**
- Insufficient gas
- Token approval needed
- Pool limits reached
- Network congestion

**Settlement Delays:**
- Anchor queue
- Dispute process
- Technical issues
- Governance votes

</div>

## Next Steps

### Deepen Your Knowledge

Continue with:
1. [Rewards System](rewards-system.md) - Detailed reward structures
2. [Due Diligence Framework](due-diligence.md) - Analysis methods
3. [Risk Management](risk-management.md) - Advanced protection

---

!!! info "Technical Note"
    Signal mechanics are continuously optimized based on ecosystem data. Stay updated with the latest parameters through official channels.

!!! warning "Risk Reminder"
    Understanding mechanics doesn't guarantee profits. Always signal within your risk tolerance and never invest more than you can afford to lose.