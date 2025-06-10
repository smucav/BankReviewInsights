# Insights and Recommendations

## Objective
Analyze 1,087 Google Play reviews (CBE: 360, BOA: 366, Dashen: 361) to derive insights, visualize sentiment/themes, and recommend app improvements.

## Insights

### Drivers
- **Ease of Use (Positive User Experience)**: Dashen (243 reviews, 67%, 4.91 avg. rating) and CBE (217 reviews, 60%, 4.81) are praised for intuitive navigation (e.g., CBE ID 2: “Best Mobile Banking app ever”).
- **Responsive Customer Service**: Dashen (29 reviews, 8%, 4.97) and CBE (11 reviews, 3%, 5.0) benefit from strong support (e.g., “better service”).

### Pain Points
- **Login/Re-registration Issues (Technical Issues)**: BOA (45 reviews, 12%, 1.13) and CBE (13 reviews, 4%, 1.77) face login errors (e.g., CBE ID 1: “physical presence for every app install”).
- **Negative User Experience**: BOA (172 reviews, 47%, 1.16) and CBE (63 reviews, 18%, 1.57) suffer from general dissatisfaction.

### Bank Comparison
- **Dashen**: Highest satisfaction (67% positive, 4.91 avg. rating), minimal technical issues (2%).
- **CBE**: Balanced (60% positive, ~3.0 avg. rating), with Feature Requests (e.g., Amharic support).
- **BOA**: Lowest satisfaction (47% negative, 2.47 avg. rating), high technical issues (12%).

## Visualizations
- **Sentiment Trends**: Monthly sentiment by bank (`plots/figures/sentiment_trends.png`).
- **Rating Distributions**: Boxplot of ratings (`plots/figures/rating_distributions.png`).
- **Theme Percentages**: Theme proportions (`plots/figures/theme_percentages.png`).
- **Keyword Clouds**: Per bank (e.g., `plots/figures/keyword_cloud_dashen_bank.png`).
- **Sentiment Distribution**: Sentiment counts (`plots/figures/sentiment_distribution.png`).

## Recommendations
- **Streamline Login/Re-registration**: BOA and CBE should use implicit app source verification (e.g., Google Play) to fix login issues (BOA: 45 reviews, CBE: 13 reviews).
- **Implement Amharic Support**: CBE should add Amharic UI to address Feature Requests (5 reviews).
- **Improve App Stability**: BOA should conduct usability testing to reduce crashes and improve UX (47% negative reviews).

## Ethical Considerations
- **Negative Skew**: Reviews over-represent dissatisfied users (BOA: 47% negative).
- **Language Bias**: Excluded Amharic reviews, missing local feedback.
- **Platform Bias**: Google Play data excludes iOS or in-person feedback.
